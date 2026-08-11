"""Simple camera referee that delegates robot motion to PlacePiece action."""

import cv2
from cv_bridge import CvBridge
import numpy as np
from project2_interfaces.action import PlacePiece
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image


class TicTacToeRefereeNode(Node):
    """Detect human pieces and request a robot placement for the next turn."""

    def __init__(self):
        super().__init__('tic_tac_toe_referee')

        self.declare_parameter('image_topic', '/gripper_camera/image_raw')
        self.declare_parameter('camera_info_topic', '/gripper_camera/camera_info')

        self.bridge = CvBridge()
        self.camera_matrix = None
        self.dist_coeffs = None
        self.board_state = [[0, 0, 0] for _ in range(3)]
        self.game_state = 'WAIT_FOR_HUMAN'
        self.pending_cell = None

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )
        if hasattr(cv2.aruco, 'DetectorParameters_create'):
            self.aruco_params = cv2.aruco.DetectorParameters_create()
        else:
            self.aruco_params = cv2.aruco.DetectorParameters()

        self.create_subscription(
            Image,
            self.get_parameter('image_topic').value,
            self.image_callback,
            10,
        )
        self.create_subscription(
            CameraInfo,
            self.get_parameter('camera_info_topic').value,
            self.info_callback,
            10,
        )
        self.place_piece_client = ActionClient(self, PlacePiece, 'place_piece')
        self.get_logger().info('틱택토 심판 노드 준비 완료')

    def info_callback(self, msg):
        """Cache calibrated camera parameters."""
        if self.camera_matrix is None:
            self.camera_matrix = np.asarray(msg.k, dtype=np.float64).reshape(3, 3)
            self.dist_coeffs = np.asarray(msg.d, dtype=np.float64)

    def image_callback(self, msg):
        """Update the human board state from ArUco observations."""
        if self.camera_matrix is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(
            gray,
            self.aruco_dict,
            parameters=self.aruco_params,
        )

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            _, translations, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners,
                0.04,
                self.camera_matrix,
                self.dist_coeffs,
            )
            for index, marker_id in enumerate(ids.flatten()):
                if not 11 <= marker_id <= 15:
                    continue
                translation = translations[index][0]
                row, column = self.get_board_cell(
                    translation[0],
                    translation[1],
                )
                if row is None or self.board_state[row][column] != 0:
                    continue
                if self.game_state != 'WAIT_FOR_HUMAN':
                    continue
                self.board_state[row][column] = 1
                self.game_state = 'ROBOT_TURN'
                self.get_logger().info(f'사람 수 감지: ({row}, {column})')

        self.draw_tictactoe_overlay(frame)
        cv2.imshow('Tic-Tac-Toe Referee', frame)
        cv2.waitKey(1)

        if self.game_state == 'ROBOT_TURN' and self.pending_cell is None:
            self.request_robot_turn()

    @staticmethod
    def get_board_cell(x, y):
        """Map a board-aligned marker position to a grid row and column."""
        if -0.15 <= x < -0.05:
            column = 0
        elif -0.05 <= x <= 0.05:
            column = 1
        elif 0.05 < x <= 0.15:
            column = 2
        else:
            return None, None

        if -0.15 <= y < -0.05:
            row = 0
        elif -0.05 <= y <= 0.05:
            row = 1
        elif 0.05 < y <= 0.15:
            row = 2
        else:
            return None, None
        return row, column

    def request_robot_turn(self):
        """Select the first empty cell and send it to the motion action server."""
        target = None
        for row in range(3):
            for column in range(3):
                if self.board_state[row][column] == 0:
                    target = row * 3 + column
                    break
            if target is not None:
                break

        if target is None:
            self.game_state = 'GAME_OVER'
            return
        if not self.place_piece_client.wait_for_server(timeout_sec=0.1):
            self.get_logger().warning('PlacePiece action server를 기다리는 중입니다.')
            return

        goal = PlacePiece.Goal()
        goal.cell_id = target
        self.pending_cell = target
        future = self.place_piece_client.send_goal_async(
            goal,
            feedback_callback=self.place_feedback_callback,
        )
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Start waiting for the placement result after goal acceptance."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('PlacePiece goal이 거부되었습니다.')
            self.pending_cell = None
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.place_result_callback)

    def place_feedback_callback(self, feedback_msg):
        """Log the current manipulator stage."""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Pick & Place: {feedback.stage} ({feedback.progress:.0f}%)'
        )

    def place_result_callback(self, future):
        """Commit the robot move only after physical execution succeeds."""
        result = future.result().result
        target = self.pending_cell
        self.pending_cell = None
        if result.success and target is not None:
            row, column = divmod(target, 3)
            self.board_state[row][column] = 2
            self.game_state = 'WAIT_FOR_HUMAN'
            self.get_logger().info(result.message)
        else:
            self.game_state = 'ERROR'
            self.get_logger().error(result.message)

    def draw_tictactoe_overlay(self, frame):
        """Draw the currently committed board state on the camera image."""
        start_x, start_y = 30, 50
        cv2.putText(
            frame,
            '--- Tic-Tac-Toe Board State ---',
            (start_x, start_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
        for row in range(3):
            for column in range(3):
                value = self.board_state[row][column]
                symbol = '.' if value == 0 else ('X' if value == 1 else 'O')
                cv2.putText(
                    frame,
                    f'[{symbol}]',
                    (start_x + column * 50, start_y + 30 + row * 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )

    def destroy_node(self):
        cv2.destroyAllWindows()
        self.place_piece_client.destroy()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = TicTacToeRefereeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
