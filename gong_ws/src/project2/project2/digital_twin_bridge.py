#!/usr/bin/env python3
"""실제 OpenManipulator-X의 /joint_states를 Gazebo 트윈으로 미러링.

계획서(디지털 트윈 요구사항): "실제 Manipulator의 /joint_states와 게임판의
BoardState를 Gazebo와 동기화하여 실제 환경과 시뮬레이션 환경을 연계한 디지털
트윈 시스템 구현". 이 노드는 그 중 관절 상태 동기화 부분을 담당한다.

실행 전제:
  - 실제 하드웨어가 네임스페이스 없이 떠 있어 /joint_states를 발행 중이어야 함
    (ros2 launch open_manipulator_bringup open_manipulator_x.launch.py use_sim:=false)
  - Gazebo 트윈은 'twin' 네임스페이스로 떠 있어야 함
    (ros2 launch project2 digital_twin.launch.py)
"""
import rclpy
from builtin_interfaces.msg import Duration
from control_msgs.action import GripperCommand
from rclpy.action import ActionClient
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

ARM_JOINTS = ['joint1', 'joint2', 'joint3', 'joint4']
GRIPPER_JOINT = 'gripper_left_joint'
# 그리퍼는 액션 인터페이스라 매 /joint_states 콜백마다 goal을 보내면
# 액션 서버에 부하가 크다. 이 정도 이상 실제로 움직였을 때만 새 goal을 보낸다.
GRIPPER_CHANGE_THRESHOLD = 0.01


class DigitalTwinBridge(Node):
    """실제 로봇의 관절 상태를 구독해 Gazebo 트윈 컨트롤러로 그대로 흘려보낸다."""

    def __init__(self):
        super().__init__('digital_twin_bridge')

        self.declare_parameter('twin_namespace', 'twin')
        namespace = self.get_parameter('twin_namespace').value

        self.arm_pub = self.create_publisher(
            JointTrajectory, f'/{namespace}/arm_controller/joint_trajectory', 10
        )
        self.gripper_client = ActionClient(
            self, GripperCommand, f'/{namespace}/gripper_controller/gripper_cmd'
        )
        self.last_gripper_position = None

        self.create_subscription(JointState, '/joint_states', self._on_joint_states, 10)
        self.get_logger().info(
            f"실제 로봇 /joint_states -> Gazebo 트윈(/{namespace}) 미러링 시작"
        )

    def _on_joint_states(self, msg: JointState):
        name_to_position = dict(zip(msg.name, msg.position))

        if all(joint in name_to_position for joint in ARM_JOINTS):
            trajectory = JointTrajectory()
            trajectory.joint_names = list(ARM_JOINTS)
            point = JointTrajectoryPoint()
            point.positions = [name_to_position[joint] for joint in ARM_JOINTS]
            point.time_from_start = Duration(sec=0, nanosec=100_000_000)
            trajectory.points = [point]
            self.arm_pub.publish(trajectory)

        if GRIPPER_JOINT in name_to_position:
            position = name_to_position[GRIPPER_JOINT]
            moved_enough = (
                self.last_gripper_position is None
                or abs(position - self.last_gripper_position) > GRIPPER_CHANGE_THRESHOLD
            )
            if moved_enough:
                self.last_gripper_position = position
                self._send_gripper_goal(position)

    def _send_gripper_goal(self, position):
        if not self.gripper_client.server_is_ready():
            return
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = 0.0
        self.gripper_client.send_goal_async(goal)


def main(args=None):
    rclpy.init(args=args)
    node = DigitalTwinBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
