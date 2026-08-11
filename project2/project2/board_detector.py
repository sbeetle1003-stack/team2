import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class BoardDetectorNode(Node):
    def __init__(self):
        super().__init__('board_detector')
        
        # 이미지 구독자 및 보드 상태 퍼블리셔 설정
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',  # 실제 카메라 혹은 Gazebo 카메라 토픽 이름
            self.image_callback,
            10
        )
        self.publisher_ = self.create_publisher(String, '/board_state', 10)
        self.bridge = CvBridge()
        
        # [수정 1] ArUco 디텍터 초기화 (OpenCV 구버전 호환)
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters_create()

        self.get_logger().info("Board Detector Node has been started.")

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f"CvBridge Error: {e}")
            return

        # 1. ArUco 마커 검출 (보드 셀 식별용 ID: 0 ~ 8)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # [수정 2] 구버전 방식으로 마커 검출 함수 직접 호출
        corners, ids, rejected = cv2.aruco.detectMarkers(
            gray, 
            self.aruco_dict, 
            parameters=self.aruco_params
        )

        # 3x3 보드 상태 초기화 (기본값: UNKNOWN)
        board_state = [['UNKNOWN' for _ in range(3)] for _ in range(3)]
        
        # 마커 ID와 3x3 셀 매핑 사전 (ID 0~8을 (row, col)로 매핑)
        id_to_cell = {
            0: (0, 0), 1: (0, 1), 2: (0, 2),
            3: (1, 0), 4: (1, 1), 5: (1, 2),
            6: (2, 0), 7: (2, 1), 8: (2, 2)
        }

        detected_ids = []
        if ids is not None:
            detected_ids = ids.flatten()

        # 2. 각 셀별 상태 판정 (ArUco 검출 여부 + HSV 색상 분석 결합)
        for marker_id, (r, c) in id_to_cell.items():
            if marker_id in detected_ids:
                cell_status = self.analyze_cell_color(cv_image, corners, detected_ids, marker_id)
                board_state[r][c] = cell_status
            else:
                board_state[r][c] = 'UNKNOWN'

        # 3. ROS2 토픽으로 보드 상태 발행
        state_msg = String()
        flat_state = [board_state[r][c] for r in range(3) for c in range(3)]
        state_msg.data = ",".join(flat_state)
        
        self.publisher_.publish(state_msg)

    def analyze_cell_color(self, image, corners, detected_ids, target_id):
        """
        HSV 색상 검출을 통해 HUMAN 또는 ROBOT의 말 색상 판별
        """
        idx = np.where(detected_ids == target_id)[0][0]
        pts = corners[idx][0].astype(int)
        
        x_min, y_min = np.min(pts, axis=0)
        x_max, y_max = np.max(pts, axis=0)
        
        h_img, w_img, _ = image.shape
        if x_min < 0 or y_min < 0 or x_max > w_img or y_max > h_img:
            return 'EMPTY'

        roi = image[y_min:y_max, x_min:x_max]
        if roi.size == 0:
            return 'EMPTY'

        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # 파란색 범위 (ROBOT 예시)
        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])
        blue_mask = cv2.inRange(hsv_roi, lower_blue, upper_blue)

        # 빨간색 범위 (HUMAN 예시)
        lower_red1 = np.array([0, 150, 50])
        upper_red1 = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv_roi, lower_red1, upper_red1)

        if np.sum(blue_mask) > 100:
            return 'ROBOT'
        elif np.sum(red_mask) > 100:
            return 'HUMAN'
        else:
            return 'EMPTY'

def main(args=None):
    rclpy.init(args=args)
    node = BoardDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()