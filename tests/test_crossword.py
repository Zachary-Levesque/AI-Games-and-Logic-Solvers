from pathlib import Path

from conftest import ROOT, load_module


crossword = load_module("crossword", "Crossword AI/crossword.py")
generate = load_module("generate", "Crossword AI/generate.py")


def test_crossword_solver_finds_assignment():
    puzzle = crossword.Crossword(
        str(ROOT / "Crossword AI/data/structure0.txt"),
        str(ROOT / "Crossword AI/data/words0.txt"),
    )
    creator = generate.CrosswordCreator(puzzle)

    assignment = creator.solve()

    assert assignment is not None
    assert creator.assignment_complete(assignment)
    assert creator.consistent(assignment)


def test_crossword_save_works_from_repo_root(tmp_path: Path):
    puzzle = crossword.Crossword(
        str(ROOT / "Crossword AI/data/structure0.txt"),
        str(ROOT / "Crossword AI/data/words0.txt"),
    )
    creator = generate.CrosswordCreator(puzzle)
    assignment = creator.solve()

    output_path = tmp_path / "crossword.png"
    creator.save(assignment, output_path)

    assert output_path.exists()
