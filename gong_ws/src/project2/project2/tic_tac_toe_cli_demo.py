#!/usr/bin/env python3
"""틱택토 가상 시뮬레이션 (터미널 콘솔용, ROS/Gazebo 없이 로직만 확인).

사람(X)이 좌표를 입력하면 로봇(O)이 minimax로 응수한다.
python3 tic_tac_toe_cli_demo.py 로 직접 실행하거나,
run_scripted_demo()로 스크립트 시나리오를 자동 재생할 수 있다.
"""

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


def print_board(board: list[list[int]]) -> None:
    for r in range(3):
        print(" ".join(SYMBOLS[board[r][c]] for c in range(3)))
    print()


def announce_result(board: list[list[int]]) -> bool:
    """게임이 끝났으면 결과를 출력하고 True를 반환한다."""
    winner = check_winner(board)
    if winner == HUMAN:
        print(">>> 사람(X) 승리!")
        return True
    if winner == ROBOT:
        print(">>> 로봇(O) 승리!")
        return True
    if is_draw(board):
        print(">>> 무승부!")
        return True
    return False


def _to_zero_indexed(one_based_row: int, one_based_col: int) -> tuple[int, int]:
    """사람에게 보여주는 1~3 좌표를 내부 0~2 인덱스로 변환한다."""
    return one_based_row - 1, one_based_col - 1


def run_interactive() -> None:
    """실제 터미널에서 사람이 직접 좌표를 입력하며 플레이한다."""
    board = [[EMPTY] * 3 for _ in range(3)]
    print("틱택토 시작! 좌표는 'row col' (1~3, 예: 2 2 = 정중앙) 형식으로 입력하세요.\n")
    print_board(board)

    while True:
        raw = input("사람(X)의 수: ").strip().split()
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

        row, col = _to_zero_indexed(row_in, col_in)
        if not is_valid_move(board, row, col):
            print("둘 수 없는 칸입니다.")
            continue

        board[row][col] = HUMAN
        print_board(board)
        if announce_result(board):
            break

        move = choose_best_move(board)
        if move is None:
            break
        r, c = move
        board[r][c] = ROBOT
        print(f"로봇(O)이 ({r + 1}, {c + 1})에 두었습니다.")
        print_board(board)
        if announce_result(board):
            break


def run_scripted_demo(human_moves: list[tuple[int, int]]) -> list[list[int]]:
    """사람의 수를 미리 정해두고 한 판을 자동으로 재생한다 (시연/디버깅용).

    human_moves: 사람이 순서대로 둘 (row, col) 목록, **1~3 기준**.
    반환값: 게임 종료 시점의 최종 board.
    """
    board = [[EMPTY] * 3 for _ in range(3)]
    print_board(board)

    for row_in, col_in in human_moves:
        row, col = _to_zero_indexed(row_in, col_in)
        if not is_valid_move(board, row, col):
            print(f"[스킵] ({row_in},{col_in})은 둘 수 없는 칸")
            continue

        board[row][col] = HUMAN
        print(f"사람(X) -> ({row_in}, {col_in})")
        print_board(board)
        if announce_result(board):
            return board

        move = choose_best_move(board)
        if move is None:
            return board
        r, c = move
        board[r][c] = ROBOT
        print(f"로봇(O) -> ({r + 1}, {c + 1})")
        print_board(board)
        if announce_result(board):
            return board

    return board


if __name__ == "__main__":
    run_interactive()
