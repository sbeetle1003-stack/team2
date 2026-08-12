#!/usr/bin/env python3
"""카메라 없이 터미널 입력으로 틱택토 게임 전체(minimax + 실제 매니퓰레이터)를 검증.

tic_tac_toe_referee.py는 카메라(/gripper_camera/image_raw) 구독이 필수라
카메라가 준비되지 않은 상태에서는 사람 수를 넣을 방법이 없다. 이 노드는
카메라 대신 터미널에 'row col'(1~3)을 입력해 사람(O) 수를 넣으면, referee와
동일하게 minimax(tic_tac_toe_ai.choose_best_move)로 로봇 수를 계산하고
PlacePiece 액션 서버(pick_place_controller)에 실제 실행을 요청한다.

실행 순서 (터미널 3개):
  1) ros2 launch project2 tictactoe_game.launch.py
  2) ros2 run project2 pick_place_controller  (launch에서 start_pick_place:=true면 자동 실행됨)
  3) ros2 run project2 tic_tac_toe_manual_test
"""
import threading

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from ros_gz_interfaces.msg import Entity
from ros_gz_interfaces.srv import SetEntityPose

from project2_interfaces.action import PlacePiece
from project2.manipulation_geometry import cell_center
from project2.tic_tac_toe_ai import (
    EMPTY,
    HUMAN,
    ROBOT,
    check_winner,
    choose_best_move,
    is_draw,
    is_valid_move,
)

SYMBOLS = {EMPTY: ".", HUMAN: "O", ROBOT: "X"}

# config/manipulation.yaml의 board_origin_x/y, cell_spacing과 일치해야 한다.
BOARD_ORIGIN_X = 0.30
BOARD_ORIGIN_Y = 0.0
CELL_SPACING = 0.08
HUMAN_MARKER_Z = 0.04  # board top surface (~0.035) + marker half-thickness
HUMAN_MARKER_COUNT = 5


class ManualTicTacToeNode(Node):
    def __init__(self):
        super().__init__('tic_tac_toe_manual_test')
        self.board_state = [[EMPTY] * 3 for _ in range(3)]
        self.game_state = "WAIT_FOR_HUMAN"
        self.pending_cell = None

        # 사람 입력 루프가 로봇 턴이 끝날 때까지 기다리는 데 쓰는 신호.
        self.turn_ready = threading.Event()
        self.turn_ready.set()

        self.place_piece_client = ActionClient(self, PlacePiece, 'place_piece')

        # 사람 수는 로봇 팔을 움직이지 않고, world에 미리 놓아둔 빨간 O
        # 마커(human_marker_0..4)를 SetEntityPose로 해당 칸에 옮겨 표시한다.
        self.human_piece_index = 0
        self.set_pose_client = self.create_client(
            SetEntityPose, '/world/tictactoe_world/set_pose'
        )

        self.get_logger().info("카메라 없이 키보드로 테스트하는 틱택토 노드가 준비되었습니다.")

    def _place_human_marker(self, row, col):
        """사람이 둔 칸에 빨간 O 마커를 옮겨 Gazebo에도 반영한다 (팔은 움직이지 않음)."""
        if self.human_piece_index >= HUMAN_MARKER_COUNT:
            self.get_logger().warning("사람 마커를 모두 사용했습니다 (표시는 생략).")
            return
        if not self.set_pose_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning("SetEntityPose 서비스를 찾을 수 없어 마커 표시를 생략합니다.")
            return

        cell_id = row * 3 + col
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

    def print_board(self):
        for row in self.board_state:
            print(" ".join(SYMBOLS[v] for v in row))
        print()

    def judge_and_advance(self, next_state_if_ongoing):
        winner = check_winner(self.board_state)
        if winner == HUMAN:
            self.get_logger().info("게임 종료: 사람(O) 승리!")
            return "GAME_OVER"
        if winner == ROBOT:
            self.get_logger().info("게임 종료: 로봇(X) 승리!")
            return "GAME_OVER"
        if is_draw(self.board_state):
            self.get_logger().info("게임 종료: 무승부!")
            return "GAME_OVER"
        return next_state_if_ongoing

    def apply_human_move(self, row_in: int, col_in: int):
        row, col = row_in - 1, col_in - 1
        if not is_valid_move(self.board_state, row, col):
            print("둘 수 없는 칸입니다.")
            return

        self.board_state[row][col] = HUMAN
        self.get_logger().info(f"사람(O)이 ({row}, {col}) 위치에 말을 놓았습니다.")
        self._place_human_marker(row, col)
        self.print_board()

        self.game_state = self.judge_and_advance("ROBOT_TURN")
        if self.game_state == "ROBOT_TURN":
            self.turn_ready.clear()
            self.request_robot_turn()

    def request_robot_turn(self):
        """minimax로 최적의 수를 계산해 PlacePiece 액션 서버에 실행을 요청한다."""
        self.get_logger().info("로봇(X)이 다음 수를 계산하고 있습니다...")
        move = choose_best_move(self.board_state)
        if move is None:
            self.game_state = "GAME_OVER"
            self.turn_ready.set()
            return
        r, c = move
        target = r * 3 + c

        if not self.place_piece_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("PlacePiece 액션 서버를 찾을 수 없습니다. pick_place_controller가 실행 중인지 확인하세요.")
            self.game_state = "ERROR"
            self.turn_ready.set()
            return

        goal = PlacePiece.Goal()
        goal.cell_id = target
        self.pending_cell = (r, c)
        future = self.place_piece_client.send_goal_async(
            goal, feedback_callback=self.place_feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("PlacePiece goal이 거부되었습니다.")
            self.pending_cell = None
            self.game_state = "ERROR"
            self.turn_ready.set()
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.place_result_callback)

    def place_feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f"Pick & Place: {feedback.stage} ({feedback.progress:.0f}%)")

    def place_result_callback(self, future):
        result = future.result().result
        target = self.pending_cell
        self.pending_cell = None
        if result.success and target is not None:
            r, c = target
            self.board_state[r][c] = ROBOT
            self.get_logger().info(f"로봇(X)이 셀 ({r}, {c})에 말을 놓았습니다. {result.message}")
            self.print_board()
            self.game_state = self.judge_and_advance("WAIT_FOR_HUMAN")
        else:
            self.get_logger().error(f"Pick & Place 실패: {result.message}")
            self.game_state = "ERROR"
        self.turn_ready.set()


def input_loop(node: ManualTicTacToeNode):
    node.print_board()
    print("사람(O) 수를 'row col' (1~3, 예: 2 2 = 정중앙) 형식으로 입력하세요.\n")
    while rclpy.ok():
        node.turn_ready.wait()
        if node.game_state == "GAME_OVER":
            print("게임이 종료되었습니다. Ctrl+C로 종료하세요.")
            break
        if node.game_state == "ERROR":
            print("로봇 팔 제어 중 오류가 발생했습니다. Ctrl+C로 종료하세요.")
            break

        try:
            raw = input("사람(O)의 수: ").strip().split()
        except EOFError:
            break

        if len(raw) != 2:
            print("형식이 잘못됐습니다. 예: 2 2")
            continue
        try:
            row_in, col_in = int(raw[0]), int(raw[1])
        except ValueError:
            print("숫자로 입력하세요.")
            continue
        if not (1 <= row_in <= 3 and 1 <= col_in <= 3):
            print("1~3 사이 값으로 입력하세요.")
            continue

        node.apply_human_move(row_in, col_in)


def main(args=None):
    rclpy.init(args=args)
    node = ManualTicTacToeNode()

    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    try:
        input_loop(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()
        spin_thread.join(timeout=2.0)
        node.destroy_node()


if __name__ == '__main__':
    main()
