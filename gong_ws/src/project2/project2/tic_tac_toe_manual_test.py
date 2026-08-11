#!/usr/bin/env python3
"""카메라 없이 터미널 입력으로 틱택토 게임 로직을 Gazebo/ROS2 환경에서 검증.

tic_tac_toe_referee.py는 카메라(/camera/image_raw) 구독이 필수라
카메라가 준비되지 않은 상태에서는 실행할 수 없다. 이 노드는 카메라 없이
ROS2 노드만 띄운 채로, 터미널에 'row col'(1~3)을 입력해 사람(X) 수를 넣으면
로봇(O) 수는 minimax(tic_tac_toe_ai.choose_best_move)로 자동 계산해
board_state 갱신 + 승패/무승부 판정까지 동일한 흐름으로 확인할 수 있다.

실행: ros2 run project2 tic_tac_toe_manual_test
(실제 MoveItPy 팔 이동은 아직 연동 전이라 board_state 갱신 로그로만 확인한다.)
"""
import threading

import rclpy
from rclpy.node import Node

from project2.tic_tac_toe_ai import (
    EMPTY,
    HUMAN,
    ROBOT,
    check_winner,
    choose_best_move,
    is_draw,
    is_valid_move,
)

SYMBOLS = {EMPTY: ".", HUMAN: "X", ROBOT: "O"}


class ManualTicTacToeNode(Node):
    def __init__(self):
        super().__init__('tic_tac_toe_manual_test')
        self.board_state = [[EMPTY] * 3 for _ in range(3)]
        self.game_state = "WAIT_FOR_HUMAN"
        self.get_logger().info("카메라 없이 키보드로 테스트하는 틱택토 노드가 준비되었습니다.")

    def print_board(self):
        for row in self.board_state:
            print(" ".join(SYMBOLS[v] for v in row))
        print()

    def judge_and_advance(self, next_state_if_ongoing):
        winner = check_winner(self.board_state)
        if winner == HUMAN:
            self.get_logger().info("게임 종료: 사람(X) 승리!")
            return "GAME_OVER"
        if winner == ROBOT:
            self.get_logger().info("게임 종료: 로봇(O) 승리!")
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
        self.get_logger().info(f"사람(X)이 ({row}, {col}) 위치에 말을 놓았습니다.")
        self.print_board()

        self.game_state = self.judge_and_advance("ROBOT_TURN")
        if self.game_state == "ROBOT_TURN":
            self.execute_robot_turn()

    def execute_robot_turn(self):
        self.get_logger().info("로봇(O)이 다음 수를 계산하고 있습니다...")
        move = choose_best_move(self.board_state)
        if move is None:
            self.game_state = "GAME_OVER"
            return

        r, c = move
        # 실제 MoveItPy 픽앤플레이스 연동은 아직 없음 -> 상태 갱신만 검증.
        self.board_state[r][c] = ROBOT
        self.get_logger().info(f"로봇(O)이 셀 ({r}, {c})에 말을 놓았습니다. (팔 이동 미연동)")
        self.print_board()

        self.game_state = self.judge_and_advance("WAIT_FOR_HUMAN")


def input_loop(node: ManualTicTacToeNode):
    node.print_board()
    print("사람(X) 수를 'row col' (1~3, 예: 2 2 = 정중앙) 형식으로 입력하세요.\n")
    while rclpy.ok():
        if node.game_state == "GAME_OVER":
            print("게임이 종료되었습니다. Ctrl+C로 종료하세요.")
            break
        try:
            raw = input("사람(X)의 수: ").strip().split()
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
