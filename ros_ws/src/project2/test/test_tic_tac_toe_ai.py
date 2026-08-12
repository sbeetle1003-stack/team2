"""tic_tac_toe_ai의 승패 판정 + minimax 로직 검증."""

from project2.tic_tac_toe_ai import (
    EMPTY,
    HUMAN,
    ROBOT,
    check_winner,
    choose_best_move,
    is_draw,
    is_game_over,
    is_valid_move,
)


def empty_board():
    return [[EMPTY] * 3 for _ in range(3)]


def test_check_winner_row():
    board = empty_board()
    board[0] = [ROBOT, ROBOT, ROBOT]
    assert check_winner(board) == ROBOT


def test_check_winner_column():
    board = empty_board()
    for r in range(3):
        board[r][1] = HUMAN
    assert check_winner(board) == HUMAN


def test_check_winner_diagonal():
    board = empty_board()
    board[0][0] = ROBOT
    board[1][1] = ROBOT
    board[2][2] = ROBOT
    assert check_winner(board) == ROBOT


def test_no_winner_on_empty_board():
    assert check_winner(empty_board()) is None


def test_is_draw_true_when_full_and_no_winner():
    board = [
        [ROBOT, HUMAN, ROBOT],
        [ROBOT, HUMAN, HUMAN],
        [HUMAN, ROBOT, ROBOT],
    ]
    assert is_draw(board) is True
    assert is_game_over(board) is True


def test_is_draw_false_when_winner_exists():
    board = empty_board()
    board[0] = [ROBOT, ROBOT, ROBOT]
    assert is_draw(board) is False


def test_is_draw_true_early_when_one_cell_left_but_undecidable():
    """빈 칸이 1개 남아도, 그 칸이 어느 줄도 완성시킬 수 없으면 조기 무승부."""
    board = [
        [EMPTY, HUMAN, ROBOT],
        [ROBOT, HUMAN, HUMAN],
        [HUMAN, ROBOT, ROBOT],
    ]
    assert check_winner(board) is None
    assert is_draw(board) is True
    assert is_game_over(board) is True
    assert choose_best_move(board) is None


def test_is_draw_false_when_two_cells_left_and_still_winnable():
    """빈 칸이 2개 이상 남으면 항상 어느 한쪽에게는 아직 이길 가능성이 있다."""
    board = [
        [HUMAN, ROBOT, EMPTY],
        [EMPTY, HUMAN, ROBOT],
        [ROBOT, HUMAN, EMPTY],
    ]
    assert check_winner(board) is None
    assert is_draw(board) is False


def test_is_valid_move():
    board = empty_board()
    board[1][1] = ROBOT
    assert is_valid_move(board, 0, 0) is True
    assert is_valid_move(board, 1, 1) is False
    assert is_valid_move(board, 3, 0) is False
    assert is_valid_move(board, -1, 0) is False


def test_choose_best_move_blocks_human_win():
    """사람이 두 개를 놓아 이기기 직전이면, 로봇은 반드시 막아야 한다."""
    board = empty_board()
    board[0][0] = HUMAN
    board[0][1] = HUMAN
    move = choose_best_move(board)
    assert move == (0, 2)


def test_choose_best_move_takes_winning_move():
    """로봇이 한 수만 더 두면 이기는 상황이면, 그 수를 선택해야 한다."""
    board = empty_board()
    board[1][0] = ROBOT
    board[1][1] = ROBOT
    board[0][0] = HUMAN
    board[2][2] = HUMAN
    move = choose_best_move(board)
    assert move == (1, 2)


def test_choose_best_move_returns_none_when_game_over():
    board = empty_board()
    board[0] = [ROBOT, ROBOT, ROBOT]
    assert choose_best_move(board) is None


def test_minimax_never_loses_full_game_vs_itself():
    """로봇이 양쪽 다 최적play를 한다고 가정하면 항상 무승부여야 한다."""
    board = empty_board()
    turn = ROBOT
    while not is_game_over(board):
        move = choose_best_move(board) if turn == ROBOT else _best_human_move(board)
        if move is None:
            break
        r, c = move
        board[r][c] = turn
        turn = HUMAN if turn == ROBOT else ROBOT

    assert check_winner(board) is None  # 무승부 (둘 다 완벽하면 아무도 못 이김)


def _best_human_move(board):
    """사람 쪽도 완벽하게 두게 하기 위해, 부호를 뒤집은 minimax를 임시로 사용."""
    from project2.tic_tac_toe_ai import _minimax, get_empty_cells

    best_score = float("inf")
    best_move = None
    for r, c in get_empty_cells(board):
        board[r][c] = HUMAN
        score = _minimax(board, 0, True)
        board[r][c] = EMPTY
        if score < best_score:
            best_score = score
            best_move = (r, c)
    return best_move
