"""Recorded-pose PlacePiece action server for the physical OpenManipulator-X."""

import threading
from pathlib import Path

import rclpy
import yaml
from ament_index_python.packages import get_package_share_directory
from control_msgs.action import FollowJointTrajectory, GripperCommand
from project2_interfaces.action import PlacePiece
from rclpy.action import (
    ActionClient,
    ActionServer,
    CancelResponse,
    GoalResponse,
)
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectoryPoint


class MotionStageError(RuntimeError):
    """Report a failed recorded-pose stage."""

    def __init__(self, stage, message):
        super().__init__(message)
        self.stage = stage


class PickPlaceController(Node):
    """Pick a supplied piece and drop it at a recorded cell pose."""

    ARM_JOINTS = ['joint1', 'joint2', 'joint3', 'joint4']

    def __init__(self):
        super().__init__('pick_place_controller')

        default_pose_file = str(
            Path(get_package_share_directory('project2'))
            / 'config'
            / 'recorded_poses.yaml'
        )
        self.declare_parameter('recorded_poses_file', default_pose_file)
        self.declare_parameter('dry_run', False)
        self.declare_parameter('piece_count', 5)

        self.dry_run = bool(self.get_parameter('dry_run').value)
        self.piece_count = int(self.get_parameter('piece_count').value)
        self.next_piece_index = 0
        self.busy = False
        self.busy_lock = threading.Lock()

        pose_file = Path(self.get_parameter('recorded_poses_file').value)
        self.pose_data = self._load_and_validate_poses(pose_file)

        callback_group = ReentrantCallbackGroup()
        self.arm_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/arm_controller/follow_joint_trajectory',
            callback_group=callback_group,
        )
        self.gripper_client = ActionClient(
            self,
            GripperCommand,
            '/gripper_controller/gripper_cmd',
            callback_group=callback_group,
        )
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
        self.get_logger().info(f'Recorded poses: {pose_file}')
        self.get_logger().info(f'PlacePiece action server 준비 완료 ({mode})')

    def _load_and_validate_poses(self, pose_file):
        if not pose_file.is_file():
            raise RuntimeError(f'기록 자세 파일이 없습니다: {pose_file}')

        with pose_file.open('r', encoding='utf-8') as stream:
            data = yaml.safe_load(stream)

        try:
            gripper = data['gripper']
            poses = data['poses']
            motion = data['motion']
            required_poses = {
                'board_view': poses['board_view'],
                'supply_grasp': poses['supply_grasp'],
                'supply_lift': poses['supply_lift'],
            }
            cells = poses['cell_drop']
            for cell_id in range(9):
                required_poses[f'cell_{cell_id}'] = cells[f'cell_{cell_id}']
        except (KeyError, TypeError) as error:
            raise RuntimeError(f'기록 자세 YAML 구조가 올바르지 않습니다: {error}') from error

        for name, pose in required_poses.items():
            arm = pose.get('arm') if isinstance(pose, dict) else None
            if not isinstance(arm, list) or len(arm) != 4:
                raise RuntimeError(f'{name}.arm에는 관절값 4개가 필요합니다.')
            pose['arm'] = [float(value) for value in arm]

        for key in ('open', 'grasp', 'max_effort'):
            gripper[key] = float(gripper[key])
        for key in (
            'supply_lift_seconds',
            'supply_grasp_seconds',
            'cell_drop_seconds',
            'return_seconds',
            'board_view_seconds',
        ):
            motion[key] = float(motion[key])

        return data

    def goal_callback(self, goal_request):
        if not 0 <= int(goal_request.cell_id) <= 8:
            self.get_logger().warning(f'유효하지 않은 Cell: {goal_request.cell_id}')
            return GoalResponse.REJECT
        with self.busy_lock:
            if self.busy or self.next_piece_index >= self.piece_count:
                return GoalResponse.REJECT
            self.busy = True
        return GoalResponse.ACCEPT

    def cancel_callback(self, _goal_handle):
        return CancelResponse.ACCEPT

    def _feedback(self, goal_handle, stage, progress):
        feedback = PlacePiece.Feedback()
        feedback.stage = stage
        feedback.progress = float(progress)
        goal_handle.publish_feedback(feedback)
        self.get_logger().info(f'[{progress:5.1f}%] {stage}')

    @staticmethod
    def _wait_future(future, timeout):
        event = threading.Event()
        future.add_done_callback(lambda _future: event.set())
        if not event.wait(timeout):
            raise TimeoutError('ROS action 응답 시간이 초과되었습니다.')
        return future.result()

    def _move_arm(self, stage, positions, seconds):
        positions = [float(value) for value in positions]
        seconds = float(seconds)
        if self.dry_run:
            self.get_logger().info(
                f'{stage}: arm={positions}, duration={seconds:.1f}s'
            )
            return

        if not self.arm_client.wait_for_server(timeout_sec=3.0):
            raise MotionStageError(stage, 'arm_controller 액션 서버가 없습니다.')

        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = self.ARM_JOINTS
        point = JointTrajectoryPoint()
        point.positions = positions
        whole_seconds = int(seconds)
        point.time_from_start.sec = whole_seconds
        point.time_from_start.nanosec = int((seconds - whole_seconds) * 1e9)
        goal.trajectory.points = [point]

        try:
            goal_handle = self._wait_future(
                self.arm_client.send_goal_async(goal),
                5.0,
            )
            if not goal_handle.accepted:
                raise MotionStageError(stage, '팔 궤적 목표가 거부되었습니다.')
            wrapped_result = self._wait_future(
                goal_handle.get_result_async(),
                seconds + 10.0,
            )
            if wrapped_result.result.error_code != 0:
                raise MotionStageError(
                    stage,
                    f'팔 컨트롤러 오류: {wrapped_result.result.error_string}',
                )
        except TimeoutError as error:
            raise MotionStageError(stage, str(error)) from error

    def _move_gripper(self, stage, position):
        position = float(position)
        effort = self.pose_data['gripper']['max_effort']
        if self.dry_run:
            self.get_logger().info(
                f'{stage}: gripper={position:.6f}, max_effort={effort:.1f}'
            )
            return

        if not self.gripper_client.wait_for_server(timeout_sec=3.0):
            raise MotionStageError(stage, 'gripper_controller 액션 서버가 없습니다.')

        goal = GripperCommand.Goal()
        goal.command.position = position
        goal.command.max_effort = effort
        try:
            goal_handle = self._wait_future(
                self.gripper_client.send_goal_async(goal),
                5.0,
            )
            if not goal_handle.accepted:
                raise MotionStageError(stage, '그리퍼 목표가 거부되었습니다.')
            self._wait_future(goal_handle.get_result_async(), 8.0)
        except TimeoutError as error:
            raise MotionStageError(stage, str(error)) from error

    def _cancel_if_requested(self, goal_handle, holding_piece):
        if not goal_handle.is_cancel_requested:
            return None
        result = PlacePiece.Result()
        result.success = False
        result.error_code = PlacePiece.Result.CANCELLED
        result.message = '취소 요청을 받았습니다.'
        if holding_piece:
            result.message += ' 말은 놓지 않고 현재 그립 상태를 유지합니다.'
        goal_handle.canceled()
        return result

    def execute_callback(self, goal_handle):
        result = PlacePiece.Result()
        holding_piece = False

        try:
            cell_id = int(goal_handle.request.cell_id)
            poses = self.pose_data['poses']
            gripper = self.pose_data['gripper']
            motion = self.pose_data['motion']
            cell_pose = poses['cell_drop'][f'cell_{cell_id}']['arm']

            stages = [
                ('OPEN_GRIPPER', 5.0, lambda: self._move_gripper(
                    'OPEN_GRIPPER', gripper['open'])),
                ('SUPPLY_LIFT', 15.0, lambda: self._move_arm(
                    'SUPPLY_LIFT', poses['supply_lift']['arm'],
                    motion['supply_lift_seconds'])),
                ('SUPPLY_GRASP', 30.0, lambda: self._move_arm(
                    'SUPPLY_GRASP', poses['supply_grasp']['arm'],
                    motion['supply_grasp_seconds'])),
                ('CLOSE_GRIPPER', 40.0, lambda: self._move_gripper(
                    'CLOSE_GRIPPER', gripper['grasp'])),
                ('LIFT_PIECE', 55.0, lambda: self._move_arm(
                    'LIFT_PIECE', poses['supply_lift']['arm'],
                    motion['supply_lift_seconds'])),
                ('CELL_DROP', 75.0, lambda: self._move_arm(
                    'CELL_DROP', cell_pose,
                    motion['cell_drop_seconds'])),
                ('RELEASE', 82.0, lambda: self._move_gripper(
                    'RELEASE', gripper['open'])),
                ('RETREAT', 92.0, lambda: self._move_arm(
                    'RETREAT', poses['supply_lift']['arm'],
                    motion['return_seconds'])),
                ('RETURN_BOARD_VIEW', 98.0, lambda: self._move_arm(
                    'RETURN_BOARD_VIEW', poses['board_view']['arm'],
                    motion['board_view_seconds'])),
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

            self.next_piece_index += 1
            goal_handle.succeed()
            result.success = True
            result.error_code = PlacePiece.Result.SUCCESS
            result.message = f'Cell {cell_id} 배치 완료'
            self._feedback(goal_handle, 'DONE', 100.0)
            return result

        except MotionStageError as error:
            self.get_logger().error(f'{error.stage} 실패: {error}')
            goal_handle.abort()
            result.success = False
            result.error_code = PlacePiece.Result.EXECUTION_FAILED
            result.message = f'{error.stage} 단계 실패: {error}'
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
        self.arm_client.destroy()
        self.gripper_client.destroy()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PickPlaceController()
    executor = MultiThreadedExecutor(num_threads=4)
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
