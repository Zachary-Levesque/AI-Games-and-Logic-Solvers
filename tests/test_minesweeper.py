from conftest import load_module


minesweeper = load_module("minesweeper", "Minesweeper AI/minesweeper.py")


def test_zero_knowledge_marks_all_neighbors_safe():
    ai = minesweeper.MinesweeperAI(height=3, width=3)
    ai.add_knowledge((1, 1), 0)

    expected_safes = {
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
    }
    assert ai.safes == expected_safes
    assert ai.mines == set()


def test_subset_inference_discovers_mine():
    ai = minesweeper.MinesweeperAI(height=3, width=3)
    ai.mark_safe((0, 0))
    ai.knowledge = [
        minesweeper.Sentence({(0, 1), (1, 0)}, 1),
        minesweeper.Sentence({(0, 1), (1, 0), (1, 1)}, 2),
    ]

    ai._infer_knowledge()

    assert (1, 1) in ai.mines
