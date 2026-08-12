"""Integration-compatible entry point for the Gazebo robot synchronizer.

The original integration branch exposes ``digital_twin_robot``.  The working
Gazebo Sim implementation is kept in ``gazebo_joint_mirror`` because it
forwards each hardware joint to the simulator's position-controller topic,
which is the interface used by the current mirror launch file.
"""

from project2.gazebo_joint_mirror import GazeboJointMirror

import rclpy


def main(args=None):
    """Run the hardware-to-Gazebo joint synchronizer."""
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


if __name__ == '__main__':
    main()
