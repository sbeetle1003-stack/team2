"""틱택토 승패 판정 + Minimax 최적수 탐색.

board_state: 3x3 list, 0=빈칸(EMPTY), 1=사람(HUMAN/O), 2=로봇(ROBOT/X).
사람이 항상 선수이며 O, 로봇은 항상 후수이며 X로 표시한다 (내부 값은
동일, 화면/로그 표시 기호만 이렇게 정한다).
tic_tac_toe_referee.py의 board_state와 동일한 값 규약을 쓴다.
ROS/Gazebo와 무관한 순수 로직이라 단독으로 임포트·테스트할 수 있다.
"""

import random

EMPTY = 0
HUMAN = 1
ROBOT = 2

# normal 난이도에서 minimax가 내다보는 최대 수(ply). 로봇 자신의 수 이후
# 기준으로, 이 수를 넘어서면 정확한 승패 대신 0(무승부 취급)으로 잘라
# 실력을 낮춘다.
NORMAL_MAX_DEPTH = 2
# easy 난이도에서 최적수 대신 완전 무작위 수를 두는 확률.
EASY_RANDOM_PROB = 0.8

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


def game_outcome(board: list[list[int]]) -> str | None:
    """게임 결과를 'HUMAN'/'ROBOT'/'DRAW' 중 하나로, 아직 진행 중이면 None으로 반환한다.

    referee.py/manual_test.py의 judge_and_advance()가 이 함수 하나로 판정하므로,
    승패/무승부 판정 정확성은 이 함수의 유닛테스트만으로 검증된다.
    """
    winner = check_winner(board)
    if winner == HUMAN:
        return 'HUMAN'
    if winner == ROBOT:
        return 'ROBOT'
    if is_draw(board):
        return 'DRAW'
    return None


def get_empty_cells(board: list[list[int]]) -> list[tuple[int, int]]:
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]


def is_valid_move(board: list[list[int]], row: int, col: int) -> bool:
    """범위 안이고 빈 칸이면 True."""
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == EMPTY


def _minimax(
    board: list[list[int]], depth: int, is_maximizing: bool, max_depth: int | None = None
) -> int:
    winner = check_winner(board)
    if winner == ROBOT:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if is_draw(board):
        return 0
    if max_depth is not None and depth >= max_depth:
        # 여기서 더 못 내다보므로 무승부로 간주하고 잘라낸다 (난이도 하향용).
        return 0

    if is_maximizing:
        best = float("-inf")
        for r, c in get_empty_cells(board):
            board[r][c] = ROBOT
            best = max(best, _minimax(board, depth + 1, False, max_depth))
            board[r][c] = EMPTY
        return best

    best = float("inf")
    for r, c in get_empty_cells(board):
        board[r][c] = HUMAN
        best = min(best, _minimax(board, depth + 1, True, max_depth))
        board[r][c] = EMPTY
    return best


def choose_best_move(
    board: list[list[int]],
    max_depth: int | None = None,
    candidates: list[tuple[int, int]] | None = None,
) -> tuple[int, int] | None:
    """로봇(O)이 둘 최적의 (row, col)을 minimax로 계산한다.

    이미 게임이 끝났거나 빈 칸이 없으면 None을 반환한다.
    승리는 최대한 빨리, 패배는 최대한 늦게 하도록 depth를 점수에 반영한다.
    max_depth를 주면 그 수만큼만 내다보고 잘라내 실력을 낮춘다(None이면 완전탐색).
    candidates를 주면 그 칸들 중에서만 고른다(None이면 빈 칸 전체).
    """
    if is_game_over(board):
        return None

    cells = candidates if candidates is not None else get_empty_cells(board)
    best_score = float("-inf")
    best_move = None
    for r, c in cells:
        board[r][c] = ROBOT
        score = _minimax(board, 0, False, max_depth)
        board[r][c] = EMPTY
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move


# easy 난이도에서 로봇의 '첫 수'(사람이 선수를 둔 직후 첫 응수)에는 두지 못하게
# 막는 네 귀퉁이 칸(1-1, 1-3, 3-1, 3-3을 0-index로 변환한 값).
EASY_FIRST_MOVE_BANNED_CELLS = {(0, 0), (0, 2), (2, 0), (2, 2)}


def _is_robots_opening_reply(board: list[list[int]]) -> bool:
    """보드에 말이 정확히 1개(사람의 첫 수)만 있어 지금이 로봇의 첫 수 차례인지."""
    placed = sum(1 for row in board for cell in row if cell != EMPTY)
    return placed == 1


def choose_move(
    board: list[list[int]], difficulty: str = "hard"
) -> tuple[int, int] | None:
    """난이도에 따라 로봇의 다음 수를 고른다.

    - easy: 대부분 무작위(EASY_RANDOM_PROB 확률), 가끔만 최적수.
      단, 로봇의 첫 수(사람 선수 직후 응수)에서는 EASY_FIRST_MOVE_BANNED_CELLS
      (네 귀퉁이)를 후보에서 제외한다.
    - normal: NORMAL_MAX_DEPTH 수만 내다보는 depth 제한 minimax.
    - hard: 완전탐색 minimax(기존 choose_best_move와 동일, 절대 안 짐).
    """
    if is_game_over(board):
        return None

    if difficulty == "easy":
        candidates = get_empty_cells(board)
        if _is_robots_opening_reply(board):
            candidates = [
                cell for cell in candidates if cell not in EASY_FIRST_MOVE_BANNED_CELLS
            ]
        if random.random() < EASY_RANDOM_PROB:
            return random.choice(candidates) if candidates else None
        return choose_best_move(board, candidates=candidates)

    if difficulty == "normal":
        return choose_best_move(board, max_depth=NORMAL_MAX_DEPTH)

    return choose_best_move(board)


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
