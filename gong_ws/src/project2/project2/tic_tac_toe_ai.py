"""틱택토 승패 판정 + Minimax 최적수 탐색.

board_state: 3x3 list, 0=빈칸(EMPTY), 1=사람(HUMAN/O), 2=로봇(ROBOT/X).
사람이 항상 선수이며 O, 로봇은 항상 후수이며 X로 표시한다 (내부 값은
동일, 화면/로그 표시 기호만 이렇게 정한다).
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


def _line_open_for(board: list[list[int]], line, player: int) -> bool:
    """해당 줄에 상대방 말이 하나도 없어 player가 아직 완성할 수 있으면 True."""
    return all(board[r][c] in (EMPTY, player) for r, c in line)


def is_draw(board: list[list[int]]) -> bool:
    """승자가 없고, 남은 8개 줄 중 어느 쪽도 완성할 수 없으면 True.

    3x3 틱택토는 보드가 다 차지 않아도(빈 칸이 1개만 남아도) 이미 결과가
    결정되는 경우가 있다. 모든 줄이 이미 양쪽 말이 섞여 죽어 있으면(둘 다
    완성 불가) 남은 빈 칸과 무관하게 무승부로 조기 판정한다. 보드가 실제로
    다 찬 경우도 이 조건의 특수한 경우라 별도 처리가 필요 없다.
    """
    if check_winner(board) is not None:
        return False
    return not any(
        _line_open_for(board, line, HUMAN) or _line_open_for(board, line, ROBOT)
        for line in WIN_LINES
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
