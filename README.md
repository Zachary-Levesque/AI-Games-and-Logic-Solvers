# AI Games and Logic Solvers

A portfolio repository of classical AI systems implemented in Python using adversarial search, reinforcement learning, logical inference, constraint satisfaction, and probabilistic ranking.

The project includes:

- `Tic Tac Toe AI`: perfect-play minimax with alpha-beta pruning.
- `Minesweeper AI`: knowledge-based inference over sentence constraints.
- `Nim`: self-play Q-learning agent.
- `Checkers`: adversarial search with alpha-beta pruning.
- `Crossword AI`: crossword generation via CSP backtracking and arc consistency.
- `Knights and Knaves Solver`: propositional logic model checking.
- `PageRank Simulation`: sampling and iterative PageRank estimation.

## Why This Repo Matters

This codebase demonstrates core AI techniques that demonstrate:

- Search and game-playing algorithms with deterministic evaluation.
- Reinforcement learning fundamentals with Q-value updates.
- Symbolic reasoning and logical entailment.
- Constraint propagation and backtracking heuristics.
- Probabilistic modeling and convergence-based ranking.
- End-to-end engineering discipline with tests, reproducible setup, and documentation.

## Repository Layout

```text
.
├── Checkers/
├── Crossword AI/
├── Knights and Knaves Solver/
├── Minesweeper AI/
├── Nim/
├── PageRank Simulation/
├── Tic Tac Toe AI/
└── tests/
```

## Quick Start

1. Create and activate a virtual environment.
2. Install the project in editable mode with development tooling.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run The Projects

```bash
python3 "PageRank Simulation/pagerank.py" "PageRank Simulation/corpus0"
python3 "Knights and Knaves Solver/puzzle.py"
python3 "Crossword AI/generate.py" "Crossword AI/data/structure0.txt" "Crossword AI/data/words0.txt"
python3 "Nim/play.py"
python3 "Checkers/main.py"
python3 "Tic Tac Toe AI/runner.py"
python3 "Minesweeper AI/runner.py"
```

## Test Suite

```bash
python3 -m pytest
```

For a fuller local validation pass, run:

```bash
python3 "PageRank Simulation/pagerank.py" "PageRank Simulation/corpus0"
python3 "Knights and Knaves Solver/puzzle.py"
python3 "Crossword AI/generate.py" "Crossword AI/data/structure0.txt" "Crossword AI/data/words0.txt" /tmp/crossword.png
```

## Notes

- The interactive `pygame` projects require a local desktop environment.
- The `pygame` runners now resolve assets relative to their own directories, so launching them from the repository root works correctly.
- The repository intentionally keeps the original project directories so each AI example remains easy to inspect independently.
