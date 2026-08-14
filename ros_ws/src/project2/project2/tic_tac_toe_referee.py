"""ROS2 referee for the tic-tac-toe robot.

Receives the physical board state from /board_state, validates turn-by-turn
board transitions, asks the AI for the robot move, and sends that move to the
PlacePiece action server.

Important recovery behavior:
- Vision updates observed while the robot action is running are not committed
  immediately, but a valid ROBOT placement at the pending cell is remembered.
- Even if the action result reports a late-stage failure (for example RELEASE),
  the referee can recover if vision has already confirmed that the robot piece
  was physically placed at the expected cell.
"""

import rclpy
from project2_interfaces.action import PlacePiece
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import Int8MultiArray

from project2.tic_tac_toe_ai import (
    check_winner,
    choose_move,
    is_draw,
)


EMPTY = 0
HUMAN = 1
ROBOT = 2
UNKNOWN = 3

WAIT_FOR_HUMAN = "WAIT_FOR_HUMAN"
ROBOT_MOVING = "ROBOT_MOVING"
WAIT_FOR_ROBOT_CONFIRMATION = "WAIT_FOR_ROBOT_CONFIRMATION"
GAME_OVER = "GAME_OVER"
ERROR = "ERROR"


class TicTacToeRefereeNode(Node):
    """Manage turns between board vision, AI, and the PlacePiece action server."""

    def __init__(self):
        super().__init__("tic_tac_toe_referee")

        self.declare_parameter('difficulty', 'hard')  # easy | normal | hard

        self.board_state = [[EMPTY, EMPTY, EMPTY] for _ in range(3)]
        self.previous_board_state = None

        self.game_state = WAIT_FOR_HUMAN
        self.pending_cell = None

        # Robot-placement observation remembered while Action is still running.
        # This is important because board_detector only publishes when the stable
        # board state changes. If the robot piece is seen before the Action result
        # arrives, there may be no second /board_state message afterward.
        self.robot_move_seen_during_action = False
        self.observed_robot_board = None

        self.create_subscription(
            Int8MultiArray,
            "/board_state",
            self.board_state_callback,
            10,
        )

        self.place_piece_client = ActionClient(
            self,
            PlacePiece,
            "place_piece",
        )

        self.get_logger().info(
            f"틱택토 심판 노드 준비 완료 (state={self.game_state})"
        )

    @staticmethod
    def copy_board(board):
        """Return a copy of a 3x3 integer board."""
        return [row.copy() for row in board]

    @staticmethod
    def detect_human_move(previous_board, new_board):
        """Return one legal HUMAN move, or None for an invalid transition.

        During WAIT_FOR_HUMAN the only legal change is exactly one
        EMPTY -> HUMAN transition. Existing pieces may not disappear/change,
        and a new ROBOT piece may not appear.
        """
        human_moves = []

        for row in range(3):
            for col in range(3):
                previous = previous_board[row][col]
                current = new_board[row][col]

                if previous == current:
                    continue

                if previous == EMPTY and current == HUMAN:
                    human_moves.append((row, col))
                    continue

                # Any other change is illegal during the human turn.
                return None

        if len(human_moves) != 1:
            return None

        return human_moves[0]

    def is_expected_robot_confirmation(self, previous_board, new_board):
        """Return True only if pending_cell changed EMPTY -> ROBOT.

        Every other cell must remain identical to the previously committed board.
        """
        if self.pending_cell is None:
            return False

        expected_row, expected_col = divmod(self.pending_cell, 3)

        for row in range(3):
            for col in range(3):
                previous = previous_board[row][col]
                current = new_board[row][col]

                if row == expected_row and col == expected_col:
                    if previous != EMPTY or current != ROBOT:
                        return False
                elif current != previous:
                    return False

        return True

    def finish_robot_confirmation(self, confirmed_board):
        """Commit a vision-confirmed robot move and advance the game."""
        if self.pending_cell is None:
            self.game_state = ERROR
            self.get_logger().error(
                "로봇 수를 확정하려 했지만 pending_cell이 없습니다."
            )
            return

        row, col = divmod(self.pending_cell, 3)

        self.board_state = self.copy_board(confirmed_board)
        self.previous_board_state = self.copy_board(confirmed_board)

        self.pending_cell = None
        self.robot_move_seen_during_action = False
        self.observed_robot_board = None

        self.get_logger().info(
            f"Robot Move confirmed: row={row}, col={col}"
        )

        winner = check_winner(self.board_state)

        if winner == ROBOT:
            self.game_state = GAME_OVER
            self.get_logger().info("Game Over: ROBOT wins")
        elif is_draw(self.board_state):
            self.game_state = GAME_OVER
            self.get_logger().info("Game Over: Draw")
        else:
            self.game_state = WAIT_FOR_HUMAN
            self.get_logger().info("사람의 다음 수를 기다립니다.")

    def board_state_callback(self, msg):
        """Validate a vision update and advance the game state."""
        if len(msg.data) != 9:
            self.get_logger().warning(
                f"잘못된 BoardState 길이: {len(msg.data)}"
            )
            return

        if UNKNOWN in msg.data:
            self.get_logger().warning(
                "UNKNOWN 상태가 포함되어 있어 BoardState를 무시합니다."
            )
            return

        new_board = [
            list(msg.data[0:3]),
            list(msg.data[3:6]),
            list(msg.data[6:9]),
        ]

        self.get_logger().info(
            f"BoardState received: {new_board} (state={self.game_state})"
        )

        # Finished/failed games do not advance automatically.
        if self.game_state in (GAME_OVER, ERROR):
            return

        # First stable camera observation becomes the baseline.
        if self.previous_board_state is None:
            self.board_state = self.copy_board(new_board)
            self.previous_board_state = self.copy_board(new_board)
            self.get_logger().info("초기 BoardState를 등록했습니다.")
            return

        # While the robot is moving, do not commit transient camera states.
        # However, remember a strictly valid placement at the AI-selected cell.
        if self.game_state == ROBOT_MOVING:
            if self.is_expected_robot_confirmation(
                self.previous_board_state,
                new_board,
            ):
                if not self.robot_move_seen_during_action:
                    row, col = divmod(self.pending_cell, 3)
                    self.get_logger().info(
                        "Action 실행 중 로봇 말 확인: "
                        f"row={row}, col={col}"
                    )

                self.robot_move_seen_during_action = True
                self.observed_robot_board = self.copy_board(new_board)

            return

        # If the Action has finished, wait for camera confirmation unless the
        # placement was already observed during ROBOT_MOVING.
        if self.game_state == WAIT_FOR_ROBOT_CONFIRMATION:
            if self.is_expected_robot_confirmation(
                self.previous_board_state,
                new_board,
            ):
                self.finish_robot_confirmation(new_board)
            else:
                self.get_logger().warning(
                    "로봇 수 확인 대기 중 비정상 BoardState를 무시합니다."
                )

            return

        # Only a legal human move may advance WAIT_FOR_HUMAN.
        if self.game_state != WAIT_FOR_HUMAN:
            self.get_logger().warning(
                f"처리할 수 없는 게임 상태입니다: {self.game_state}"
            )
            return

        move = self.detect_human_move(
            self.previous_board_state,
            new_board,
        )

        if move is None:
            self.get_logger().warning(
                "Invalid board transition. BoardState를 무시합니다."
            )
            return

        row, col = move

        self.board_state = self.copy_board(new_board)
        self.previous_board_state = self.copy_board(new_board)

        self.get_logger().info(
            f"Human Move: row={row}, col={col}"
        )

        winner = check_winner(self.board_state)

        if winner == HUMAN:
            self.game_state = GAME_OVER
            self.get_logger().info("Game Over: HUMAN wins")
            return

        if is_draw(self.board_state):
            self.game_state = GAME_OVER
            self.get_logger().info("Game Over: Draw")
            return

        self.request_robot_turn()

    def request_robot_turn(self):
        """Ask the AI for the next move and send it to the action server."""
        difficulty = self.get_parameter('difficulty').value
        move = choose_move(self.board_state, difficulty)

        if move is None:
            self.game_state = GAME_OVER
            self.get_logger().info("AI가 둘 수 있는 수가 없습니다.")
            return

        row, column = move
        target = row * 3 + column

        self.get_logger().info(
            f"AI Best Move: row={row}, col={column}, cell={target}"
        )

        if not self.place_piece_client.wait_for_server(timeout_sec=0.1):
            self.game_state = ERROR
            self.get_logger().error(
                "PlacePiece action server를 찾을 수 없습니다."
            )
            return

        goal = PlacePiece.Goal()
        goal.cell_id = target

        self.pending_cell = target
        self.robot_move_seen_during_action = False
        self.observed_robot_board = None
        self.game_state = ROBOT_MOVING

        future = self.place_piece_client.send_goal_async(
            goal,
            feedback_callback=self.place_feedback_callback,
        )
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Wait for the result after the action goal is accepted."""
        try:
            goal_handle = future.result()
        except Exception as error:
            self.pending_cell = None
            self.robot_move_seen_during_action = False
            self.observed_robot_board = None
            self.game_state = ERROR
            self.get_logger().error(
                f"PlacePiece goal 요청 실패: {error}"
            )
            return

        if not goal_handle.accepted:
            self.pending_cell = None
            self.robot_move_seen_during_action = False
            self.observed_robot_board = None
            self.game_state = ERROR
            self.get_logger().error(
                "PlacePiece goal이 거부되었습니다."
            )
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.place_result_callback)

    def place_feedback_callback(self, feedback_msg):
        """Log the current pick-and-place stage."""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f"Pick & Place: {feedback.stage} ({feedback.progress:.0f}%)"
        )

    def place_result_callback(self, future):
        """Resolve an Action result using vision as the final source of truth.

        A late-stage Action failure does not immediately stop the game.
        If the expected robot piece was already seen by vision while the action
        was running, that physical placement is accepted and the game continues.
        Otherwise the referee waits for a later camera confirmation.
        """
        try:
            result = future.result().result
        except Exception as error:
            self.get_logger().warning(
                f"PlacePiece result 처리 실패: {error} "
                "- 카메라로 실제 배치 여부를 확인합니다."
            )

            if self.pending_cell is None:
                self.game_state = ERROR
                self.get_logger().error(
                    "확인할 pending_cell이 없어 복구할 수 없습니다."
                )
                return

            if (
                self.robot_move_seen_during_action
                and self.observed_robot_board is not None
            ):
                self.get_logger().info(
                    "Action result 오류가 있었지만 "
                    "이미 Vision으로 로봇 배치를 확인했습니다."
                )
                self.finish_robot_confirmation(
                    self.observed_robot_board
                )
            else:
                self.game_state = WAIT_FOR_ROBOT_CONFIRMATION
                self.get_logger().warning(
                    "로봇 말의 카메라 확인을 기다립니다."
                )

            return

        if self.pending_cell is None:
            self.game_state = ERROR
            self.get_logger().error(
                "확인할 pending_cell이 없습니다."
            )
            return

        if result.success:
            self.get_logger().info(
                f"{result.message} - 최종 배치 상태를 확인합니다."
            )
        else:
            self.get_logger().warning(
                f"{result.message} - Action은 실패했지만 "
                "Vision으로 실제 배치 여부를 확인합니다."
            )

        # board_detector may already have published the robot placement while
        # the Action was still running. Since it publishes only changed stable
        # states, waiting for another identical message could deadlock.
        if (
            self.robot_move_seen_during_action
            and self.observed_robot_board is not None
        ):
            self.get_logger().info(
                "Action 실행 중 확인된 Vision 결과로 "
                "로봇 수를 확정합니다."
            )
            self.finish_robot_confirmation(
                self.observed_robot_board
            )
            return

        self.game_state = WAIT_FOR_ROBOT_CONFIRMATION
        self.get_logger().warning(
            "아직 로봇 말이 확인되지 않았습니다. "
            "카메라 확인을 기다립니다."
        )

    def destroy_node(self):
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


if __name__ == "__main__":
    main()
