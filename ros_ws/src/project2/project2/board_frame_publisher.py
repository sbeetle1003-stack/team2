"""Publish a board-centered TF from four corner ArUco markers.

Physical marker layout:

    ID 0 ---------------- ID 1
      |                    |
      |     GAME BOARD     |
      |                    |
    ID 3 ---------------- ID 2

The resulting board_frame:
- origin: center of the four marker centers
- +x: top edge -> bottom edge
- +y: left edge -> right edge
- +z: board surface normal
"""

import numpy as np
import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import (
    Buffer,
    ConnectivityException,
    ExtrapolationException,
    LookupException,
    TransformBroadcaster,
    TransformListener,
)


TF_LOOKUP_ERRORS = (
    LookupException,
    ConnectivityException,
    ExtrapolationException,
)


def rotation_matrix_to_quaternion(matrix: np.ndarray):
    """Convert a 3x3 rotation matrix to quaternion (x, y, z, w)."""
    matrix = np.asarray(matrix, dtype=np.float64).reshape(3, 3)

    trace = float(np.trace(matrix))

    if trace > 0.0:
        s = np.sqrt(trace + 1.0) * 2.0
        qw = 0.25 * s
        qx = (matrix[2, 1] - matrix[1, 2]) / s
        qy = (matrix[0, 2] - matrix[2, 0]) / s
        qz = (matrix[1, 0] - matrix[0, 1]) / s

    elif matrix[0, 0] > matrix[1, 1] and matrix[0, 0] > matrix[2, 2]:
        s = np.sqrt(
            1.0
            + matrix[0, 0]
            - matrix[1, 1]
            - matrix[2, 2]
        ) * 2.0

        qw = (matrix[2, 1] - matrix[1, 2]) / s
        qx = 0.25 * s
        qy = (matrix[0, 1] + matrix[1, 0]) / s
        qz = (matrix[0, 2] + matrix[2, 0]) / s

    elif matrix[1, 1] > matrix[2, 2]:
        s = np.sqrt(
            1.0
            + matrix[1, 1]
            - matrix[0, 0]
            - matrix[2, 2]
        ) * 2.0

        qw = (matrix[0, 2] - matrix[2, 0]) / s
        qx = (matrix[0, 1] + matrix[1, 0]) / s
        qy = 0.25 * s
        qz = (matrix[1, 2] + matrix[2, 1]) / s

    else:
        s = np.sqrt(
            1.0
            + matrix[2, 2]
            - matrix[0, 0]
            - matrix[1, 1]
        ) * 2.0

        qw = (matrix[1, 0] - matrix[0, 1]) / s
        qx = (matrix[0, 2] + matrix[2, 0]) / s
        qy = (matrix[1, 2] + matrix[2, 1]) / s
        qz = 0.25 * s

    quaternion = np.array(
        [qx, qy, qz, qw],
        dtype=np.float64,
    )

    norm = np.linalg.norm(quaternion)

    if norm > 0.0:
        quaternion /= norm

    return quaternion


class BoardFramePublisher(Node):
    """Create board_frame from ArUco markers 0, 1, 2, and 3."""

    def __init__(self):
        super().__init__("board_frame_publisher")

        self.declare_parameter(
            "camera_optical_frame",
            "camera_optical",
        )
        self.declare_parameter(
            "board_frame_id",
            "board_frame",
        )
        self.declare_parameter(
            "publish_rate",
            30.0,
        )

        self.camera_frame = self.get_parameter(
            "camera_optical_frame"
        ).value

        self.board_frame = self.get_parameter(
            "board_frame_id"
        ).value

        self.marker_frames = {
            0: "aruco_marker_0",  # top-left
            1: "aruco_marker_1",  # top-right
            2: "aruco_marker_2",  # bottom-right
            3: "aruco_marker_3",  # bottom-left
        }

        self.buffer = Buffer()
        self.listener = TransformListener(
            self.buffer,
            self,
        )
        self.broadcaster = TransformBroadcaster(self)

        publish_rate = float(
            self.get_parameter("publish_rate").value
        )

        self.timer = self.create_timer(
            1.0 / publish_rate,
            self._on_timer,
        )

        self.get_logger().info(
            "board_frame_publisher started: "
            "markers [0,1,2,3] -> board_frame"
        )

    def _lookup_marker_position(self, marker_id):
        """Return marker center in camera_optical coordinates."""
        frame = self.marker_frames[marker_id]

        try:
            transform = self.buffer.lookup_transform(
                self.camera_frame,
                frame,
                Time(),
            )
        except TF_LOOKUP_ERRORS:
            return None, None

        translation = transform.transform.translation

        position = np.array(
            [
                translation.x,
                translation.y,
                translation.z,
            ],
            dtype=np.float64,
        )

        return position, transform.header.stamp

    def _on_timer(self):
        positions = {}
        stamps = []

        # All four corner markers must currently be visible.
        for marker_id in (0, 1, 2, 3):
            position, stamp = self._lookup_marker_position(
                marker_id
            )

            if position is None:
                return

            positions[marker_id] = position
            stamps.append(stamp)

        p0 = positions[0]  # top-left
        p1 = positions[1]  # top-right
        p2 = positions[2]  # bottom-right
        p3 = positions[3]  # bottom-left

        # --------------------------------------------------------------
        # 1. Board center
        # --------------------------------------------------------------
        board_center = (
            p0 + p1 + p2 + p3
        ) / 4.0

        # --------------------------------------------------------------
        # 2. Midpoints of the four sides
        # --------------------------------------------------------------
        top_mid = (p0 + p1) / 2.0
        bottom_mid = (p3 + p2) / 2.0

        left_mid = (p0 + p3) / 2.0
        right_mid = (p1 + p2) / 2.0

        # --------------------------------------------------------------
        # 3. Board axes
        #
        # +x : top -> bottom
        # +y : left -> right
        # --------------------------------------------------------------
        x_axis = bottom_mid - top_mid
        y_axis_raw = right_mid - left_mid

        x_norm = np.linalg.norm(x_axis)
        y_norm = np.linalg.norm(y_axis_raw)

        if x_norm < 1e-6 or y_norm < 1e-6:
            self.get_logger().warning(
                "Board marker geometry is degenerate."
            )
            return

        x_axis = x_axis / x_norm
        y_axis_raw = y_axis_raw / y_norm

        # Surface normal
        z_axis = np.cross(
            x_axis,
            y_axis_raw,
        )

        z_norm = np.linalg.norm(z_axis)

        if z_norm < 1e-6:
            self.get_logger().warning(
                "Could not determine board normal."
            )
            return

        z_axis = z_axis / z_norm

        # Recompute y so the frame is perfectly orthogonal.
        y_axis = np.cross(
            z_axis,
            x_axis,
        )

        y_axis /= np.linalg.norm(y_axis)

        # --------------------------------------------------------------
        # 4. Rotation matrix
        #
        # Columns are board_frame axes expressed in camera coordinates.
        # --------------------------------------------------------------
        rotation_matrix = np.column_stack(
            (
                x_axis,
                y_axis,
                z_axis,
            )
        )

        quaternion = rotation_matrix_to_quaternion(
            rotation_matrix
        )

        # --------------------------------------------------------------
        # 5. Publish camera_optical -> board_frame
        # --------------------------------------------------------------
        board_tf = TransformStamped()

        # Marker TFs all originate from camera frames at nearly the
        # same image time. Use the latest available stamp.
        board_tf.header.stamp = stamps[-1]
        board_tf.header.frame_id = self.camera_frame
        board_tf.child_frame_id = self.board_frame

        board_tf.transform.translation.x = float(
            board_center[0]
        )
        board_tf.transform.translation.y = float(
            board_center[1]
        )
        board_tf.transform.translation.z = float(
            board_center[2]
        )

        board_tf.transform.rotation.x = float(
            quaternion[0]
        )
        board_tf.transform.rotation.y = float(
            quaternion[1]
        )
        board_tf.transform.rotation.z = float(
            quaternion[2]
        )
        board_tf.transform.rotation.w = float(
            quaternion[3]
        )

        self.broadcaster.sendTransform(board_tf)


def main(args=None):
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


if __name__ == "__main__":
    main()