"""ROS 2 publisher for the gripper-mounted USB camera.

Publishes:
    /gripper_camera/image_raw
    /gripper_camera/camera_info

The camera is mounted on the manipulator and represented by the
`camera_link` TF frame. Intrinsics below are temporary placeholders,
not calibrated -- good enough for a rough demo, not for precise picking.
"""

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


class GripperCameraPublisher(Node):
    """Publish frames from the gripper-mounted USB camera."""

    def __init__(self):
        super().__init__('gripper_camera_pub')

        self.declare_parameter('camera_index', 0)
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)
        self.declare_parameter('fps', 30)

        self.camera_index = self.get_parameter('camera_index').value
        self.width = self.get_parameter('width').value
        self.height = self.get_parameter('height').value
        self.fps = self.get_parameter('fps').value

        self.image_pub = self.create_publisher(Image, '/gripper_camera/image_raw', 10)
        self.camera_info_pub = self.create_publisher(
            CameraInfo, '/gripper_camera/camera_info', 10
        )

        self.bridge = CvBridge()

        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise RuntimeError(f'카메라 /dev/video{self.camera_index}을 열 수 없습니다.')

        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.get_logger().info(
            f'Gripper camera opened: /dev/video{self.camera_index} '
            f'({actual_width}x{actual_height} @ {actual_fps:.1f}fps)'
        )

        self.camera_info = self._create_camera_info()
        self.timer = self.create_timer(1.0 / self.fps, self._publish_frame)

    def _create_camera_info(self) -> CameraInfo:
        msg = CameraInfo()
        msg.width = self.width
        msg.height = self.height
        msg.distortion_model = 'plumb_bob'
        msg.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        fx = fy = 600.0
        cx = self.width / 2.0
        cy = self.height / 2.0
        msg.k = [fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0]
        msg.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        msg.p = [fx, 0.0, cx, 0.0, 0.0, fy, cy, 0.0, 0.0, 0.0, 1.0, 0.0]
        return msg

    def _publish_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('카메라 프레임을 읽지 못했습니다.', throttle_duration_sec=2.0)
            return

        stamp = self.get_clock().now().to_msg()
        image_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        image_msg.header.stamp = stamp
        image_msg.header.frame_id = 'camera_link'
        self.camera_info.header.stamp = stamp
        self.camera_info.header.frame_id = 'camera_link'

        self.image_pub.publish(image_msg)
        self.camera_info_pub.publish(self.camera_info)

    def destroy_node(self):
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
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
