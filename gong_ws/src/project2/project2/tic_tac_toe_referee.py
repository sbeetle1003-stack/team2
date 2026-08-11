#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np
from geometry_msgs.msg import Pose
from moveit.planning import MoveItPy
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive

from project2.tic_tac_toe_ai import check_winner, choose_best_move, is_draw

class TicTacToeRefereeNode(Node):
    def __init__(self):
        super().__init__('tic_tac_toe_referee')
        
        # 1. MoveItPy 초기화
        self.moveit = MoveItPy(node_name="tictactoe_moveit")
        self.arm = self.moveit.get_planning_component("arm")
        self.gripper = self.moveit.get_planning_component("gripper")
        
        # 2. Planning Scene에 테이블 장애물 추가 (SDF 스펙과 동일하게 맞춤)
        self.add_table_collision()
        
        # 3. 카메라 및 ArUco 비전 설정
        self.bridge = CvBridge()
        self.sub_img = self.create_subscription(Image, "/camera/image_raw", self.image_callback, 10)
        self.sub_info = self.create_subscription(CameraInfo, "/camera/camera_info", self.info_callback, 10)
        
        self.camera_matrix = None
        self.dist_coeffs = None

        # ArUco 딕셔너리 (4x4_50)
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()

        # 3x3 틱택토 보드 상태 (0: 빈칸, 1: 사람(X), 2: 로봇(O))
        self.board_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        
        # 게임 상태 머신 ("WAIT_FOR_HUMAN" -> "ROBOT_TURN" -> "GAME_OVER")
        self.game_state = "WAIT_FOR_HUMAN"
        
        self.get_logger().info("틱택토 심판 및 로봇팔 제어 노드가 준비되었습니다.")

    def add_table_collision(self):
        planning_scene_monitor = self.moveit.get_planning_scene_monitor()
        collision_object = CollisionObject()
        collision_object.header.frame_id = "link1"
        collision_object.id = "tictactoe_table"
        
        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.8, 0.8, 0.05]  # SDF 테이블 크기와 일치
        
        box_pose = Pose()
        box_pose.position.x = 0.3
        box_pose.position.y = 0.0
        box_pose.position.z = -0.025
        
        collision_object.primitives.append(box)
        collision_object.primitive_poses.append(box_pose)
        collision_object.operation = CollisionObject.ADD
        
        planning_scene_monitor.process_collision_object(collision_object)

    def info_callback(self, msg: CameraInfo):
        if self.camera_matrix is None:
            self.camera_matrix = np.array(msg.k, dtype=np.float64).reshape(3, 3)
            self.dist_coeffs = np.array(msg.d, dtype=np.float64)

    def image_callback(self, msg: Image):
        if self.camera_matrix is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, encoding="bgr8")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ArUco 마커 검출
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.03, self.camera_matrix, self.dist_coeffs)

            for i, marker_id in enumerate(ids.flatten()):
                t = tvecs[i][0]  # [x, y, z] 카메라 좌표계 기준 마커 위치
                
                player_type = None
                symbol = ""
                # 규칙 적용: 11~15는 사람 (X), 6~10은 로봇 (O)
                if 11 <= marker_id <= 15:
                    player_type = "HUMAN"
                    symbol = "X"
                elif 6 <= marker_id <= 10:
                    player_type = "ROBOT"
                    symbol = "O"

                if player_type:
                    # 화면에 ID 및 심볼 오버레이
                    text = f"ID:{marker_id} ({symbol})"
                    cv2.putText(frame, text, (int(corners[i][0][0][0]), int(corners[i][0][0][1] - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # 3x3 보드판 셀 위치 판정
                    cell_r, cell_c = self.get_board_cell(t[0], t[1])
                    if cell_r is not None and cell_c is not None:
                        if self.board_state[cell_r][cell_c] == 0:
                            if player_type == "HUMAN":
                                self.board_state[cell_r][cell_c] = 1  # 사람 입력 (X)
                                self.get_logger().info(f"사람(X)이 ({cell_r}, {cell_c}) 위치에 말을 놓았습니다.")
                                self.game_state = self.judge_and_advance("ROBOT_TURN")

        # 화면에 현재 틱택토 보드 상태 표시 창 렌더링
        self.draw_tictactoe_overlay(frame)
        cv2.imshow("Tic-Tac-Toe Referee", frame)
        if cv2.waitKey(1) == ord('q'):
            raise KeyboardInterrupt

        # 로봇 턴일 경우 실행
        if self.game_state == "ROBOT_TURN":
            self.execute_robot_turn()

    def get_board_cell(self, x, y):
        """ 마커의 3차원 위치를 3x3 그리드 인덱스로 매핑 """
        if -0.15 <= x < -0.05: col = 0
        elif -0.05 <= x <= 0.05: col = 1
        elif 0.05 < x <= 0.15: col = 2
        else: return None, None

        if -0.15 <= y < -0.05: row = 0
        elif -0.05 <= y <= 0.05: row = 1
        elif 0.05 < y <= 0.15: row = 2
        else: return None, None

        return row, col

    def draw_tictactoe_overlay(self, frame):
        """ 영상 상단에 3x3 보드 상태('X', 'O')를 시각적으로 렌더링 """
        start_x, start_y = 30, 50
        cv2.putText(frame, "--- Tic-Tac-Toe Board State ---", (start_x, start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        for r in range(3):
            for c in range(3):
                val = self.board_state[r][c]
                char = "."
                if val == 1: char = "X"      # 사람
                elif val == 2: char = "O"    # 로봇
                
                cell_text = f"[{char}]"
                cv2.putText(frame, cell_text, (start_x + c * 50, start_y + 30 + r * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    def judge_and_advance(self, next_state_if_ongoing):
        """ 매 수를 둔 직후 승패/무승부를 판정하고, 끝났으면 GAME_OVER로 전이한다. """
        winner = check_winner(self.board_state)
        if winner == 1:
            self.get_logger().info("게임 종료: 사람(X) 승리!")
            return "GAME_OVER"
        if winner == 2:
            self.get_logger().info("게임 종료: 로봇(O) 승리!")
            return "GAME_OVER"
        if is_draw(self.board_state):
            self.get_logger().info("게임 종료: 무승부!")
            return "GAME_OVER"
        return next_state_if_ongoing

    def execute_robot_turn(self):
        """ 로봇(O)이 minimax로 최적의 수를 계산해 말을 놓는 로직 수행 """
        self.get_logger().info("로봇(O)이 다음 수를 계산하고 있습니다...")

        move = choose_best_move(self.board_state)
        if move is None:
            self.get_logger().info("더 이상 둘 수 있는 칸이 없습니다. 게임 종료!")
            self.game_state = "GAME_OVER"
            return

        target_r, target_c = move

        # 목표 좌표 매핑
        target_x = 0.3 + (target_c - 1) * 0.08
        target_y = (target_r - 1) * 0.08

        self.get_logger().info(f"로봇 목표 위치: 셀({target_r}, {target_c}) -> X:{target_x:.2f}, Y:{target_y:.2f}")

        try:
            # MoveItPy를 활용한 그리퍼 및 관절 제어 (필요에 따라 픽앤플레이스 포즈 지정)
            self.board_state[target_r][target_c] = 2  # 로봇 입력 (O)
            self.get_logger().info(f"로봇(O)이 셀 ({target_r}, {target_c})에 말을 놓았습니다.")
        except Exception as e:
            self.get_logger().error(f"로봇 제어 중 오류 발생: {e}")

        self.game_state = self.judge_and_advance("WAIT_FOR_HUMAN")

def main(args=None):
    rclpy.init(args=args)
    node = TicTacToeRefereeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()