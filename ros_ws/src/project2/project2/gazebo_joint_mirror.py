"""Mirror real OpenManipulator-X joint states into Gazebo command topics."""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64


ARM_JOINTS = ('joint1', 'joint2', 'joint3', 'joint4')
GRIPPER_JOINTS = ('gripper_left_joint', 'gripper_right_joint')


class GazeboJointMirror(Node):
    """Forward hardware joint feedback to a command-only Gazebo model."""

    def __init__(self):
        super().__init__('gazebo_joint_mirror')
        self.declare_parameter('source_topic', '/joint_states')
        self.declare_parameter(
            'sim_state_topic', '/digital_twin/joint_states'
        )
        self.declare_parameter('command_prefix', '/digital_twin')
        self.declare_parameter('report_period', 1.0)

        command_prefix = self.get_parameter('command_prefix').value.rstrip('/')
        self.publishers_by_joint = {
            joint: self.create_publisher(
                Float64, f'{command_prefix}/{joint}/cmd_pos', 10
            )
            for joint in ARM_JOINTS + GRIPPER_JOINTS
        }
        self.hardware_positions = {}
        self.sim_positions = {}
        self.message_count = 0

        self.create_subscription(
            JointState,
            self.get_parameter('source_topic').value,
            self._hardware_callback,
            10,
        )
        self.create_subscription(
            JointState,
            self.get_parameter('sim_state_topic').value,
            self._sim_callback,
            10,
        )
        self.create_timer(
            float(self.get_parameter('report_period').value),
            self._report_tracking_error,
        )
        self.get_logger().info(
            'Waiting for real /joint_states; Gazebo is command-only.'
        )

    @staticmethod
    def _positions(message):
        return {
            name: position
            for name, position in zip(message.name, message.position)
            if math.isfinite(position)
        }

    def _hardware_callback(self, message):
        positions = self._positions(message)
        if not all(joint in positions for joint in ARM_JOINTS):
            return

        self.hardware_positions = positions
        for joint in ARM_JOINTS:
            command = Float64()
            command.data = float(positions[joint])
            self.publishers_by_joint[joint].publish(command)

        if 'gripper_left_joint' in positions:
            gripper_position = float(positions['gripper_left_joint'])
            for joint in GRIPPER_JOINTS:
                command = Float64()
                command.data = gripper_position
                self.publishers_by_joint[joint].publish(command)

        self.message_count += 1
        if self.message_count == 1:
            self.get_logger().info(
                'Real joint states received; Gazebo mirroring started.'
            )

    def _sim_callback(self, message):
        self.sim_positions = self._positions(message)

    def _report_tracking_error(self):
        comparable = [
            joint
            for joint in ARM_JOINTS + ('gripper_left_joint',)
            if joint in self.hardware_positions and joint in self.sim_positions
        ]
        if not comparable:
            return
        errors = {
            joint: abs(
                self.hardware_positions[joint] - self.sim_positions[joint]
            )
            for joint in comparable
        }
        worst_joint = max(errors, key=errors.get)
        self.get_logger().info(
            f'tracking max error={errors[worst_joint]:.4f} '
            f'({worst_joint})'
        )


def main(args=None):
    rclpy.init(args=args)
    node = GazeboJointMirror()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

