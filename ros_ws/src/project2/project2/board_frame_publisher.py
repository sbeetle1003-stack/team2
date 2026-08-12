"""Re-publish a single board-reference ArUco marker as a stable `board_frame`.

`multi_aruco_tf_sub` already broadcasts `camera_optical -> aruco_marker_N`
for every marker it sees, including a fixed marker mounted on the board
itself. This node aliases that one marker as `board_frame` so downstream
consumers (cell coordinate lookups) do not need to know which physical
marker ID represents the board.
"""

import math

from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import ConnectivityException, ExtrapolationException, LookupException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf2_ros.transform_listener import TransformListener

TF_LOOKUP_ERRORS = (LookupException, ConnectivityException, ExtrapolationException)


def _yaw_quaternion(yaw):
    half = yaw * 0.5
    return (0.0, 0.0, math.sin(half), math.cos(half))


def _quaternion_multiply(q1, q2):
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    return (
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
    )


class BoardFramePublisher(Node):
    """Alias `camera_optical -> aruco_marker_<board_marker_id>` as `board_frame`."""

    def __init__(self):
        """Declare parameters and set up the TF listener/broadcaster."""
        super().__init__('board_frame_publisher')

        self.declare_parameter('camera_optical_frame', 'camera_optical')
        self.declare_parameter('board_frame_id', 'board_frame')
        self.declare_parameter('board_marker_id', 0)
        self.declare_parameter('board_marker_yaw_offset', 0.0)
        self.declare_parameter('publish_rate', 30.0)

        self.camera_frame = self.get_parameter('camera_optical_frame').value
        self.board_frame = self.get_parameter('board_frame_id').value
        self.yaw_offset = self.get_parameter('board_marker_yaw_offset').value
        marker_id = self.get_parameter('board_marker_id').value
        self.marker_frame = f'aruco_marker_{marker_id}'

        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.broadcaster = TransformBroadcaster(self)
        self.last_published_stamp = None

        rate = self.get_parameter('publish_rate').value
        self.timer = self.create_timer(1.0 / rate, self._on_timer)

        self.get_logger().info(
            f'board_frame_publisher: {self.marker_frame} -> {self.board_frame} '
            f'(yaw_offset={self.yaw_offset:.3f} rad)'
        )

    def _on_timer(self):
        try:
            marker_tf = self.buffer.lookup_transform(
                self.camera_frame, self.marker_frame, Time(),
            )
        except TF_LOOKUP_ERRORS:
            return

        if marker_tf.header.stamp == self.last_published_stamp:
            return

        board_tf = TransformStamped()
        board_tf.header.stamp = marker_tf.header.stamp
        board_tf.header.frame_id = self.camera_frame
        board_tf.child_frame_id = self.board_frame
        board_tf.transform.translation = marker_tf.transform.translation

        rotation = marker_tf.transform.rotation
        if self.yaw_offset != 0.0:
            corrected = _quaternion_multiply(
                (rotation.x, rotation.y, rotation.z, rotation.w),
                _yaw_quaternion(self.yaw_offset),
            )
            (
                board_tf.transform.rotation.x,
                board_tf.transform.rotation.y,
                board_tf.transform.rotation.z,
                board_tf.transform.rotation.w,
            ) = corrected
        else:
            board_tf.transform.rotation = rotation

        self.broadcaster.sendTransform(board_tf)
        self.last_published_stamp = marker_tf.header.stamp


def main(args=None):
    """Run the board_frame_publisher node until interrupted."""
    rclpy.init(args=args)
    node = BoardFramePublisher()
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
