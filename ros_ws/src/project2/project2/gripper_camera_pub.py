"""ROS 2 publisher for the gripper-mounted USB camera.

Publishes:
    /gripper_camera/image_raw
    /gripper_camera/camera_info

The camera is mounted on the manipulator and represented by the
`camera_link` TF frame.
"""

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


class GripperCameraPublisher(Node):
    """Publish frames from the gripper-mounted USB camera."""

    def __init__(self):
        super().__init__("gripper_camera_pub")

        # ------------------------------------------------------------------
        # Camera configuration
        # ------------------------------------------------------------------
        self.camera_index = 0
        self.width = 640
        self.height = 480
        self.fps = 30

        # ------------------------------------------------------------------
        # ROS publishers
        # ------------------------------------------------------------------
        self.image_pub = self.create_publisher(
            Image,
            "/gripper_camera/image_raw",
            10,
        )

        self.camera_info_pub = self.create_publisher(
            CameraInfo,
            "/gripper_camera/camera_info",
            10,
        )

        self.bridge = CvBridge()

        # ------------------------------------------------------------------
        # Open USB camera
        # ------------------------------------------------------------------
        self.cap = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_V4L2,
        )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        if not self.cap.isOpened():
            raise RuntimeError(
                f"카메라 /dev/video{self.camera_index}을 열 수 없습니다."
            )

        # Actual values accepted by the camera.
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.get_logger().info(
            f"Gripper camera opened: /dev/video{self.camera_index}"
        )
        self.get_logger().info(
            f"Resolution: {actual_width}x{actual_height}, "
            f"FPS: {actual_fps:.1f}"
        )

        # ------------------------------------------------------------------
        # CameraInfo
        # ------------------------------------------------------------------
        self.camera_info = self.create_camera_info()

        # 30 Hz publishing timer
        self.timer = self.create_timer(
            1.0 / self.fps,
            self.publish_frame,
        )

        self.get_logger().info(
            "Gripper camera publisher 준비 완료"
        )
        self.get_logger().info(
            "Image topic: /gripper_camera/image_raw"
        )
        self.get_logger().info(
            "CameraInfo topic: /gripper_camera/camera_info"
        )

    def create_camera_info(self) -> CameraInfo:
        """Create temporary camera intrinsic information.

        These intrinsic values are approximate and should later be
        replaced with calibrated values for accurate ArUco pose estimation.
        """
        msg = CameraInfo()

        msg.width = self.width
        msg.height = self.height
        msg.distortion_model = "plumb_bob"

        # Temporary distortion coefficients
        msg.d = [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]

        # Temporary intrinsic parameters
        fx = 600.0
        fy = 600.0
        cx = self.width / 2.0
        cy = self.height / 2.0

        # Camera intrinsic matrix K
        msg.k = [
            fx, 0.0, cx,
            0.0, fy, cy,
            0.0, 0.0, 1.0,
        ]

        # Rectification matrix R
        msg.r = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        ]

        # Projection matrix P
        msg.p = [
            fx, 0.0, cx, 0.0,
            0.0, fy, cy, 0.0,
            0.0, 0.0, 1.0, 0.0,
        ]

        return msg

    def publish_frame(self):
        """Capture and publish one camera frame."""
        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warning(
                "카메라 프레임을 읽지 못했습니다.",
                throttle_duration_sec=2.0,
            )
            return

        # Ensure the published CameraInfo matches the actual frame size.
        height, width = frame.shape[:2]

        if (
            self.camera_info.width != width
            or self.camera_info.height != height
        ):
            self.get_logger().warning(
                f"실제 카메라 해상도가 설정과 다릅니다: "
                f"{width}x{height}"
            )

        stamp = self.get_clock().now().to_msg()

        # OpenCV BGR -> ROS Image
        image_msg = self.bridge.cv2_to_imgmsg(
            frame,
            encoding="bgr8",
        )

        image_msg.header.stamp = stamp
        image_msg.header.frame_id = "camera_link"

        self.camera_info.header.stamp = stamp
        self.camera_info.header.frame_id = "camera_link"

        self.image_pub.publish(image_msg)
        self.camera_info_pub.publish(self.camera_info)

    def destroy_node(self):
        """Release camera resources before shutting down."""
        if self.cap is not None:
            self.cap.release()

        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = None

    try:
        node = GripperCameraPublisher()
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    except Exception as error:
        if node is not None:
            node.get_logger().error(str(error))
        else:
            print(f"Gripper camera publisher error: {error}")

    finally:
        if node is not None:
            node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()