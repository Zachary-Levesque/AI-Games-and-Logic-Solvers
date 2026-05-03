from conftest import load_module


board_module = load_module("board", "Checkers/board.py")
ai_module = load_module("ai", "Checkers/ai.py")


def test_piece_promotion_only_counts_once():
    board = board_module.Board()
    piece = board.get_piece(2, 1)

    board.move(piece, 7, 0)
    assert piece.king is True
    assert board.white_kings == 1

    board.move(piece, 0, 1)
    assert board.white_kings == 1


def test_winner_detected_when_player_has_no_pieces():
    board = board_module.Board()
    board.red_left = 0

    assert board.winner() == "white"


def test_alpha_beta_returns_candidate_move():
    board = board_module.Board()

    score, move = ai_module.alpha_beta(board, 2, float("-inf"), float("inf"), True, None)

    assert move is not None
    assert isinstance(score, (int, float))
