"""Simple camera referee that delegates robot motion to PlacePiece action."""

import cv2
from cv_bridge import CvBridge
import numpy as np
from project2_interfaces.action import PlacePiece
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from ros_gz_interfaces.msg import Entity
from ros_gz_interfaces.srv import SetEntityPose
from sensor_msgs.msg import CameraInfo, Image

from project2.manipulation_geometry import cell_center
from project2.tic_tac_toe_ai import HUMAN, ROBOT, check_winner, choose_best_move, is_draw

# config/manipulation.yaml의 board_origin_x/y, cell_spacing과 일치해야 한다.
BOARD_ORIGIN_X = 0.30
BOARD_ORIGIN_Y = 0.0
CELL_SPACING = 0.08
HUMAN_MARKER_Z = 0.05  # matches config/manipulation.yaml piece_rest_z for the same thin-cylinder pieces
HUMAN_MARKER_COUNT = 5


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

        # 사람 수는 로봇 팔을 움직이지 않고, world에 미리 놓아둔 빨간 O
        # 마커(human_marker_0..4)를 SetEntityPose로 해당 칸에 옮겨 표시한다.
        self.human_piece_index = 0
        self.set_pose_client = self.create_client(
            SetEntityPose, '/world/tictactoe_world/set_pose'
        )

        self.get_logger().info('틱택토 심판 노드 준비 완료')

    def _place_human_marker(self, row, column):
        """사람이 둔 칸에 빨간 O 마커를 옮겨 Gazebo에도 반영한다 (팔은 움직이지 않음)."""
        if self.human_piece_index >= HUMAN_MARKER_COUNT:
            self.get_logger().warning('사람 마커를 모두 사용했습니다 (표시는 생략).')
            return
        if not self.set_pose_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning('SetEntityPose 서비스를 찾을 수 없어 마커 표시를 생략합니다.')
            return

        cell_id = row * 3 + column
        x, y = cell_center(cell_id, BOARD_ORIGIN_X, BOARD_ORIGIN_Y, CELL_SPACING)
        request = SetEntityPose.Request()
        request.entity.name = f'human_marker_{self.human_piece_index}'
        request.entity.type = Entity.MODEL
        request.pose.position.x = float(x)
        request.pose.position.y = float(y)
        request.pose.position.z = float(HUMAN_MARKER_Z)
        request.pose.orientation.w = 1.0
        self.set_pose_client.call_async(request)
        self.human_piece_index += 1

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
                self.board_state[row][column] = HUMAN
                self.get_logger().info(f'사람 수 감지: ({row}, {column})')
                self._place_human_marker(row, column)
                self.game_state = self.judge_and_advance('ROBOT_TURN')

        self.draw_tictactoe_overlay(frame)
        cv2.imshow('Tic-Tac-Toe Referee', frame)
        cv2.waitKey(1)

        if self.game_state == 'ROBOT_TURN' and self.pending_cell is None:
            self.request_robot_turn()

    @staticmethod
    def get_board_cell(x, y):
        """Map a board-aligned marker position to a grid row and column.

        NOTE: x/y here are marker translations relative to the camera, not
        world/board_origin coordinates, so this hasn't been re-verified
        against the column mirror now used in manipulation_geometry.cell_center
        (this path is unused while the camera is offline). Re-check column
        direction against a live camera before relying on this again.
        """
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

    def judge_and_advance(self, next_state_if_ongoing):
        """Check for a win/draw after a move and transition to GAME_OVER if so."""
        winner = check_winner(self.board_state)
        if winner == HUMAN:
            self.get_logger().info('게임 종료: 사람(O) 승리!')
            return 'GAME_OVER'
        if winner == ROBOT:
            self.get_logger().info('게임 종료: 로봇(X) 승리!')
            return 'GAME_OVER'
        if is_draw(self.board_state):
            self.get_logger().info('게임 종료: 무승부!')
            return 'GAME_OVER'
        return next_state_if_ongoing

    def request_robot_turn(self):
        """Ask minimax for the robot's optimal move and send it to the motion action server."""
        move = choose_best_move(self.board_state)
        if move is None:
            self.game_state = 'GAME_OVER'
            return
        target = move[0] * 3 + move[1]

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
            self.board_state[row][column] = ROBOT
            self.get_logger().info(result.message)
            self.game_state = self.judge_and_advance('WAIT_FOR_HUMAN')
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
                symbol = '.' if value == 0 else ('O' if value == 1 else 'X')
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
