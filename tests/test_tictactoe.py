from conftest import load_module


tictactoe = load_module("tictactoe", "Tic Tac Toe AI/tictactoe.py")


def test_result_rejects_out_of_bounds_move():
    board = tictactoe.initial_state()
    try:
        tictactoe.result(board, (3, 3))
    except ValueError as exc:
        assert "out of bounds" in str(exc)
    else:
        raise AssertionError("Expected ValueError for out-of-bounds move")


def test_minimax_finds_immediate_win_for_x():
    board = [
        [tictactoe.X, tictactoe.X, tictactoe.EMPTY],
        [tictactoe.O, tictactoe.O, tictactoe.EMPTY],
        [tictactoe.EMPTY, tictactoe.EMPTY, tictactoe.EMPTY],
    ]
    assert tictactoe.minimax(board) == (0, 2)
