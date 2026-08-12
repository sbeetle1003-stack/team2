import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ArucoTfPublisher(Node):
    def __init__(self):
        super().__init__('aruco_tf_publisher')
        self.subscription = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10
        )
        self.bridge = CvBridge()
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.get_logger().info("ArUco TF Publisher Node가 시작되었습니다.")

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)
        
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
        cv2.imshow("ArUco Tic-Tac-Toe Detection", frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ArucoTfPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.try_shutdown()

if __name__ == '__main__':
    main()