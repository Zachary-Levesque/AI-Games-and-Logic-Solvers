from conftest import load_module


def test_tictactoe_runner_imports_without_starting_game_loop():
    runner = load_module("tictactoe_runner", "Tic Tac Toe AI/runner.py")
    assert hasattr(runner, "main")


def test_minesweeper_runner_imports_without_starting_game_loop():
    runner = load_module("minesweeper_runner", "Minesweeper AI/runner.py")
    assert hasattr(runner, "main")


def test_nim_play_module_exposes_main():
    play_module = load_module("nim_play", "Nim/play.py")
    assert hasattr(play_module, "main")
