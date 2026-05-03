from conftest import load_module


puzzle = load_module("puzzle", "Knights and Knaves Solver/puzzle.py")
logic = load_module("logic", "Knights and Knaves Solver/logic.py")


def test_puzzle_knowledge_matches_expected_solution():
    assert logic.model_check(puzzle.knowledge0, puzzle.AKnave)
    assert logic.model_check(puzzle.knowledge1, puzzle.BKnight)
    assert logic.model_check(puzzle.knowledge3, puzzle.CKnight)
