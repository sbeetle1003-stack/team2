"""MoveIt 2 action server for OpenManipulator-X tic-tac-toe placement."""

import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import rclpy
import xacro
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import Pose, PoseStamped
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_msgs.msg import CollisionObject
from project2_interfaces.action import PlacePiece
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from ros_gz_interfaces.msg import Entity
from ros_gz_interfaces.srv import SetEntityPose
from shape_msgs.msg import SolidPrimitive
from std_msgs.msg import Empty

from project2.manipulation_geometry import cell_center, supply_position


class MotionStageError(RuntimeError):
    """Describe which motion stage failed and how it failed."""

    def __init__(self, stage, execution=False):
        super().__init__(stage)
        self.stage = stage
        self.execution = execution


class PickPlaceController(Node):
    """Execute deterministic pick-and-place stages through MoveItPy."""

    def __init__(self):
        super().__init__('pick_place_controller')

        self.declare_parameter('base_frame', 'link1')
        self.declare_parameter('tool_frame', 'end_effector_link')
        self.declare_parameter('board_origin_x', 0.30)
        self.declare_parameter('board_origin_y', 0.0)
        self.declare_parameter('cell_spacing', 0.08)
        self.declare_parameter('supply_x', 0.10)
        self.declare_parameter('supply_y', -0.20)
        self.declare_parameter('supply_spacing', 0.05)
        self.declare_parameter('piece_count', 5)
        self.declare_parameter('pre_grasp_z', 0.15)
        self.declare_parameter('grasp_z', 0.075)
        self.declare_parameter('lift_z', 0.15)
        self.declare_parameter('pre_place_z', 0.15)
        self.declare_parameter('place_z', 0.075)
        self.declare_parameter('retreat_z', 0.15)
        self.declare_parameter('orientation_x', 0.0)
        self.declare_parameter('orientation_y', 0.0)
        self.declare_parameter('orientation_z', 0.0)
        self.declare_parameter('orientation_w', 1.0)
        self.declare_parameter('return_home', True)
        self.declare_parameter('add_table_collision', False)
        self.declare_parameter('simulate_piece_attachment', True)
        self.declare_parameter('piece_rest_z', 0.025)
        self.declare_parameter('dry_run', False)

        self.base_frame = self.get_parameter('base_frame').value
        self.tool_frame = self.get_parameter('tool_frame').value
        self.board_origin_x = self.get_parameter('board_origin_x').value
        self.board_origin_y = self.get_parameter('board_origin_y').value
        self.cell_spacing = self.get_parameter('cell_spacing').value
        self.supply_x = self.get_parameter('supply_x').value
        self.supply_y = self.get_parameter('supply_y').value
        self.supply_spacing = self.get_parameter('supply_spacing').value
        self.piece_count = self.get_parameter('piece_count').value
        self.dry_run = self.get_parameter('dry_run').value
        self.return_home = self.get_parameter('return_home').value
        self.simulate_piece_attachment = self.get_parameter(
            'simulate_piece_attachment'
        ).value

        self.orientation = (
            self.get_parameter('orientation_x').value,
            self.get_parameter('orientation_y').value,
            self.get_parameter('orientation_z').value,
            self.get_parameter('orientation_w').value,
        )

        self.next_piece_index = 0
        self.busy = False
        self.busy_lock = threading.Lock()

        self.get_logger().info('MoveItPy 초기화를 시작합니다.')
        moveit_config = (
            MoveItConfigsBuilder(
                robot_name='open_manipulator_x',
                package_name='open_manipulator_moveit_config',
            )
            .robot_description_semantic(
                str(
                    Path('config')
                    / 'open_manipulator_x'
                    / 'open_manipulator_x.srdf'
                )
            )
            .joint_limits(
                str(Path('config') / 'open_manipulator_x' / 'joint_limits.yaml')
            )
            .trajectory_execution(
                str(
                    Path('config')
                    / 'open_manipulator_x'
                    / 'moveit_controllers.yaml'
                )
            )
            .robot_description_kinematics(
                str(Path('config') / 'open_manipulator_x' / 'kinematics.yaml')
            )
            .to_moveit_configs()
        )
        config_dict = moveit_config.to_dict()
        # The stock simulation URDF gives the wrist-mounted camera a collision
        # box which overlaps link5 by about 0.3 mm at otherwise valid poses.
        # Keep the camera visual/sensor in Gazebo, but remove only that geometry
        # from this node's planning model so IK goals are not falsely rejected.
        description_share = get_package_share_directory(
            'open_manipulator_description'
        )
        robot_description = xacro.process_file(
            str(
                Path(description_share)
                / 'urdf'
                / 'open_manipulator_x'
                / 'open_manipulator_x.urdf.xacro'
            ),
            mappings={'use_sim': 'true'},
        ).toxml()
        robot_root = ET.fromstring(robot_description)
        camera_link = robot_root.find("./link[@name='camera_link']")
        if camera_link is not None:
            for collision in camera_link.findall('collision'):
                camera_link.remove(collision)
        config_dict['robot_description'] = ET.tostring(
            robot_root,
            encoding='unicode',
        )
        config_dict['robot_description_semantic'] = config_dict[
            'robot_description_semantic'
        ].replace(
            '</robot>',
            '  <disable_collisions link1="camera_link" link2="link1" '
            'reason="SensorMount"/>\n'
            '  <disable_collisions link1="camera_link" link2="link2" '
            'reason="SensorMount"/>\n'
            '  <disable_collisions link1="camera_link" link2="link3" '
            'reason="SensorMount"/>\n'
            '  <disable_collisions link1="camera_link" link2="link4" '
            'reason="Adjacent"/>\n'
            '  <disable_collisions link1="camera_link" link2="link5" '
            'reason="Adjacent"/>\n'
            '  <disable_collisions link1="camera_link" '
            'link2="end_effector_link" reason="Adjacent"/>\n'
            '  <disable_collisions link1="camera_link" '
            'link2="gripper_left_link" reason="Adjacent"/>\n'
            '  <disable_collisions link1="camera_link" '
            'link2="gripper_right_link" reason="Adjacent"/>\n'
            '</robot>',
        )
        pipeline_names = config_dict['planning_pipelines']
        config_dict['planning_pipelines'] = {
            'pipeline_names': pipeline_names,
            'namespace': '',
        }
        config_dict['plan_request_params'] = {
            'planning_attempts': 5,
            'planning_pipeline': 'ompl',
            'planner_id': 'RRTConnectkConfigDefault',
            'planning_time': 5.0,
            'max_velocity_scaling_factor': 0.5,
            'max_acceleration_scaling_factor': 0.5,
        }
        config_dict['use_sim_time'] = self.get_parameter('use_sim_time').value
        config_dict['qos_overrides'] = {
            '/clock': {
                'subscription': {
                    'depth': 1,
                    'durability': 'volatile',
                    'history': 'keep_last',
                    'reliability': 'best_effort',
                }
            }
        }
        self.moveit = MoveItPy(
            node_name='project2_moveit_py',
            config_dict=config_dict,
        )
        self.arm = self.moveit.get_planning_component('arm')
        self.gripper = self.moveit.get_planning_component('gripper')
        if self.get_parameter('add_table_collision').value:
            self._add_table_collision()

        self.attach_publishers = []
        self.detach_publishers = []
        self.initial_detach_count = 0
        self.initial_detach_timer = None
        if self.simulate_piece_attachment:
            self.piece_pose_client = self.create_client(
                SetEntityPose,
                '/world/tictactoe_world/set_pose',
            )
            for marker_id in range(6, 6 + self.piece_count):
                piece_name = f'robot_cube_{marker_id}'
                self.attach_publishers.append(
                    self.create_publisher(Empty, f'/{piece_name}/attach', 10)
                )
                self.detach_publishers.append(
                    self.create_publisher(Empty, f'/{piece_name}/detach', 10)
                )
            # A DetachableJoint starts attached. Re-publish a few times to
            # cover Gazebo / DDS discovery without moving the home-position arm.
            self.initial_detach_timer = self.create_timer(
                0.5,
                self._detach_all_initial_pieces,
            )

        callback_group = ReentrantCallbackGroup()
        self.action_server = ActionServer(
            self,
            PlacePiece,
            'place_piece',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=callback_group,
        )
        mode = 'DRY-RUN' if self.dry_run else 'EXECUTE'
        self.get_logger().info(f'PlacePiece action server 준비 완료 ({mode})')

    def _add_table_collision(self):
        """Add the table as a collision object in the MoveIt planning scene."""
        collision_object = CollisionObject()
        collision_object.header.frame_id = self.base_frame
        collision_object.id = 'tictactoe_table'

        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.48, 0.8, 0.05]

        box_pose = Pose()
        box_pose.position.x = 0.30
        box_pose.position.y = 0.0
        box_pose.position.z = -0.025

        collision_object.primitives.append(box)
        collision_object.primitive_poses.append(box_pose)
        collision_object.operation = CollisionObject.ADD

        monitor = self.moveit.get_planning_scene_monitor()
        monitor.process_collision_object(collision_object)

    def goal_callback(self, goal_request):
        """Reject invalid, concurrent, or out-of-pieces goals immediately."""
        if not 0 <= goal_request.cell_id <= 8:
            self.get_logger().warning(f'유효하지 않은 Cell: {goal_request.cell_id}')
            return GoalResponse.REJECT
        with self.busy_lock:
            if self.busy or self.next_piece_index >= self.piece_count:
                return GoalResponse.REJECT
            self.busy = True
        return GoalResponse.ACCEPT

    def cancel_callback(self, _goal_handle):
        """Accept cancellation and stop at the next safe stage boundary."""
        return CancelResponse.ACCEPT

    def _feedback(self, goal_handle, stage, progress):
        feedback = PlacePiece.Feedback()
        feedback.stage = stage
        feedback.progress = float(progress)
        goal_handle.publish_feedback(feedback)
        self.get_logger().info(f'[{progress:5.1f}%] {stage}')

    def _detach_all_initial_pieces(self):
        for publisher in self.detach_publishers:
            publisher.publish(Empty())
        self.initial_detach_count += 1
        if self.initial_detach_count >= 4 and self.initial_detach_timer is not None:
            self.initial_detach_timer.cancel()

    def _attach_piece(self, piece_index):
        if not self.simulate_piece_attachment:
            return
        self.attach_publishers[piece_index].publish(Empty())
        time.sleep(0.15)
        self.get_logger().info(f'Gazebo piece {piece_index} attached')

    def _detach_piece(self, piece_index):
        if not self.simulate_piece_attachment:
            return
        self.detach_publishers[piece_index].publish(Empty())
        time.sleep(0.15)
        self.get_logger().info(f'Gazebo piece {piece_index} detached')

    def _close_and_attach(self, piece_index):
        self._move_named(self.gripper, 'close', 'CLOSE_GRIPPER')
        self._attach_piece(piece_index)

    def _set_piece_pose(self, piece_index, target_x, target_y):
        if not self.piece_pose_client.wait_for_service(timeout_sec=2.0):
            raise MotionStageError('RELEASE', execution=True)
        request = SetEntityPose.Request()
        request.entity.name = f'robot_cube_{piece_index + 6}'
        request.entity.type = Entity.MODEL
        request.pose.position.x = float(target_x)
        request.pose.position.y = float(target_y)
        request.pose.position.z = float(
            self.get_parameter('piece_rest_z').value
        )
        request.pose.orientation.w = 1.0
        future = self.piece_pose_client.call_async(request)
        deadline = time.monotonic() + 2.0
        while not future.done() and time.monotonic() < deadline:
            time.sleep(0.02)
        if not future.done() or not future.result().success:
            raise MotionStageError('RELEASE', execution=True)

    def _open_and_detach(self, piece_index, target_x, target_y):
        self._move_named(self.gripper, 'open', 'RELEASE')
        self._detach_piece(piece_index)
        if self.simulate_piece_attachment:
            self._set_piece_pose(piece_index, target_x, target_y)

    def _pose(self, x, y, z):
        pose = PoseStamped()
        pose.header.frame_id = self.base_frame
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = float(z)
        pose.pose.orientation.x = float(self.orientation[0])
        pose.pose.orientation.y = float(self.orientation[1])
        pose.pose.orientation.z = float(self.orientation[2])
        pose.pose.orientation.w = float(self.orientation[3])
        return pose

    def _set_arm_start_state_to_current(self):
        """Use current feedback while tolerating tiny encoder limit overshoot."""
        self.arm.set_start_state_to_current_state()
        start_state = self.arm.get_start_state()
        if start_state is None:
            return

        # The physical arm's joint4 feedback can overshoot its URDF lower
        # bound by a few milliradians after a trajectory. MoveIt rejects the
        # next plan before execution even though the controller's 0.01 rad
        # start tolerance can safely accept that difference. Clamp only the
        # planning copy; the real feedback and commanded trajectory remain
        # unchanged.
        lower = np.array([-np.pi, -1.5, -1.5, -1.7], dtype=float)
        upper = np.array([np.pi, 1.5, 1.4, 1.97], dtype=float)
        positions = np.asarray(
            start_state.get_joint_group_positions('arm'),
            dtype=float,
        )
        bounded = np.clip(positions, lower, upper)
        if not np.allclose(positions, bounded, atol=1e-9):
            self.get_logger().warn(
                '현재 피드백이 관절 한계를 소폭 벗어나 계획용 상태만 보정합니다: '
                f'{positions.tolist()} -> {bounded.tolist()}'
            )
            start_state.set_joint_group_positions('arm', bounded)
            start_state.update()
            self.arm.set_start_state(robot_state=start_state)

    def _move_arm(self, stage, target_pose):
        if self.dry_run:
            self.get_logger().info(
                f'{stage}: ({target_pose.pose.position.x:.3f}, '
                f'{target_pose.pose.position.y:.3f}, '
                f'{target_pose.pose.position.z:.3f})'
            )
            return

        self._set_arm_start_state_to_current()
        goal_state = RobotState(self.moveit.get_robot_model())
        ik_found = goal_state.set_from_ik(
            'arm',
            target_pose.pose,
            self.tool_frame,
            1.0,
        )
        if not ik_found:
            self.get_logger().error(f'{stage}: 역기구학 해를 찾지 못했습니다.')
            raise MotionStageError(stage)
        goal_state.update()
        self.arm.set_goal_state(robot_state=goal_state)
        plan_result = self.arm.plan()
        if not plan_result:
            raise MotionStageError(stage)

        try:
            execution_result = self.moveit.execute(
                plan_result.trajectory,
                controllers=[],
            )
            if not execution_result:
                self.get_logger().error(
                    f'{stage} 실행 결과가 실패했습니다: {execution_result}'
                )
                raise MotionStageError(stage, execution=True)
        except Exception as error:
            self.get_logger().error(f'{stage} 실행 오류: {error}')
            raise MotionStageError(stage, execution=True) from error

    def _move_named(self, component, target_name, stage):
        if self.dry_run:
            self.get_logger().info(f'{stage}: named target={target_name}')
            return

        if component is self.arm:
            self._set_arm_start_state_to_current()
        else:
            component.set_start_state_to_current_state()
        component.set_goal_state(configuration_name=target_name)
        plan_result = component.plan()
        if not plan_result:
            raise MotionStageError(stage)

        try:
            execution_result = self.moveit.execute(
                plan_result.trajectory,
                controllers=[],
            )
            if not execution_result:
                self.get_logger().error(
                    f'{stage} 실행 결과가 실패했습니다: {execution_result}'
                )
                raise MotionStageError(stage, execution=True)
        except Exception as error:
            self.get_logger().error(f'{stage} 실행 오류: {error}')
            raise MotionStageError(stage, execution=True) from error

    @staticmethod
    def _cancelled_result(goal_handle, message):
        result = PlacePiece.Result()
        result.success = False
        result.error_code = PlacePiece.Result.CANCELLED
        result.message = message
        goal_handle.canceled()
        return result

    def _cancel_if_requested(self, goal_handle, holding_piece=False):
        if not goal_handle.is_cancel_requested:
            return None
        message = '취소 요청을 받았습니다.'
        if holding_piece:
            message += ' 말은 놓지 않고 현재 그립 상태를 유지합니다.'
        return self._cancelled_result(goal_handle, message)

    def execute_callback(self, goal_handle):
        """Execute the full pre-grasp through retreat sequence."""
        result = PlacePiece.Result()
        holding_piece = False

        try:
            cell_id = int(goal_handle.request.cell_id)
            target_x, target_y = cell_center(
                cell_id,
                self.board_origin_x,
                self.board_origin_y,
                self.cell_spacing,
            )
            pick_x, pick_y = supply_position(
                self.next_piece_index,
                self.supply_x,
                self.supply_y,
                self.supply_spacing,
            )

            stages = [
                ('OPEN_GRIPPER', 5.0, lambda: self._move_named(
                    self.gripper, 'open', 'OPEN_GRIPPER')),
                ('PRE_GRASP', 15.0, lambda: self._move_arm(
                    'PRE_GRASP', self._pose(pick_x, pick_y,
                                            self.get_parameter('pre_grasp_z').value))),
                ('GRASP_APPROACH', 30.0, lambda: self._move_arm(
                    'GRASP_APPROACH', self._pose(pick_x, pick_y,
                                                self.get_parameter('grasp_z').value))),
                ('CLOSE_GRIPPER', 40.0, lambda: self._close_and_attach(
                    self.next_piece_index)),
                ('LIFT', 52.0, lambda: self._move_arm(
                    'LIFT', self._pose(pick_x, pick_y,
                                      self.get_parameter('lift_z').value))),
                ('PRE_PLACE', 68.0, lambda: self._move_arm(
                    'PRE_PLACE', self._pose(target_x, target_y,
                                           self.get_parameter('pre_place_z').value))),
                ('PLACE', 80.0, lambda: self._move_arm(
                    'PLACE', self._pose(target_x, target_y,
                                       self.get_parameter('place_z').value))),
                ('RELEASE', 86.0, lambda: self._open_and_detach(
                    self.next_piece_index, target_x, target_y)),
                ('RETREAT', 94.0, lambda: self._move_arm(
                    'RETREAT', self._pose(target_x, target_y,
                                         self.get_parameter('retreat_z').value))),
            ]

            for stage, progress, operation in stages:
                cancelled = self._cancel_if_requested(goal_handle, holding_piece)
                if cancelled is not None:
                    return cancelled
                self._feedback(goal_handle, stage, progress)
                operation()
                if stage == 'CLOSE_GRIPPER':
                    holding_piece = True
                elif stage == 'RELEASE':
                    holding_piece = False

            if self.return_home:
                self._feedback(goal_handle, 'RETURN_HOME', 98.0)
                self._move_named(self.arm, 'home', 'RETURN_HOME')

            self.next_piece_index += 1
            goal_handle.succeed()
            result.success = True
            result.error_code = PlacePiece.Result.SUCCESS
            result.message = f'Cell {cell_id} 배치 완료'
            self._feedback(goal_handle, 'DONE', 100.0)
            return result

        except MotionStageError as error:
            goal_handle.abort()
            result.success = False
            result.error_code = (
                PlacePiece.Result.EXECUTION_FAILED
                if error.execution
                else PlacePiece.Result.PLAN_FAILED
            )
            result.message = f'{error.stage} 단계 실패'
            return result
        except Exception as error:
            self.get_logger().error(f'예상하지 못한 Pick & Place 오류: {error}')
            goal_handle.abort()
            result.success = False
            result.error_code = PlacePiece.Result.ROBOT_NOT_READY
            result.message = str(error)
            return result
        finally:
            with self.busy_lock:
                self.busy = False

    def destroy_node(self):
        self.action_server.destroy()
        self.moveit.shutdown()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PickPlaceController()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
