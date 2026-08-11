"""틱택토 승패 판정 + Minimax 최적수 탐색.

board_state: 3x3 list, 0=빈칸(EMPTY), 1=사람(HUMAN/X), 2=로봇(ROBOT/O).
tic_tac_toe_referee.py의 board_state와 동일한 값 규약을 쓴다.
ROS/Gazebo와 무관한 순수 로직이라 단독으로 임포트·테스트할 수 있다.
"""

EMPTY = 0
HUMAN = 1
ROBOT = 2

WIN_LINES = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


def check_winner(board: list[list[int]]) -> int | None:
    """승자가 있으면 HUMAN 또는 ROBOT, 없으면 None을 반환한다."""
    for line in WIN_LINES:
        values = [board[r][c] for r, c in line]
        if values[0] != EMPTY and values[0] == values[1] == values[2]:
            return values[0]
    return None


def is_draw(board: list[list[int]]) -> bool:
    """승자 없이 보드가 다 찼으면 True."""
    return check_winner(board) is None and all(
        cell != EMPTY for row in board for cell in row
    )


def is_game_over(board: list[list[int]]) -> bool:
    return check_winner(board) is not None or is_draw(board)


def get_empty_cells(board: list[list[int]]) -> list[tuple[int, int]]:
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]


def is_valid_move(board: list[list[int]], row: int, col: int) -> bool:
    """범위 안이고 빈 칸이면 True."""
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == EMPTY


def _minimax(board: list[list[int]], depth: int, is_maximizing: bool) -> int:
    winner = check_winner(board)
    if winner == ROBOT:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best = float("-inf")
        for r, c in get_empty_cells(board):
            board[r][c] = ROBOT
            best = max(best, _minimax(board, depth + 1, False))
            board[r][c] = EMPTY
        return best

    best = float("inf")
    for r, c in get_empty_cells(board):
        board[r][c] = HUMAN
        best = min(best, _minimax(board, depth + 1, True))
        board[r][c] = EMPTY
    return best


def choose_best_move(board: list[list[int]]) -> tuple[int, int] | None:
    """로봇(O)이 둘 최적의 (row, col)을 minimax로 계산한다.

    이미 게임이 끝났거나 빈 칸이 없으면 None을 반환한다.
    승리는 최대한 빨리, 패배는 최대한 늦게 하도록 depth를 점수에 반영한다.
    """
    if is_game_over(board):
        return None

    best_score = float("-inf")
    best_move = None
    for r, c in get_empty_cells(board):
        board[r][c] = ROBOT
        score = _minimax(board, 0, False)
        board[r][c] = EMPTY
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move


if __name__ == "__main__":
    # 간단한 수동 확인용 데모
    demo_board = [
        [ROBOT, HUMAN, ROBOT],
        [HUMAN, ROBOT, EMPTY],
        [EMPTY, EMPTY, HUMAN],
    ]
    print("보드:", demo_board)
    print("승자:", check_winner(demo_board))
    print("무승부:", is_draw(demo_board))
    print("로봇 다음 수:", choose_best_move(demo_board))
