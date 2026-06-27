# Connect-N AI — CPSC 481 Project

An AI agent for Connect Four and configurable Connect-N variants using Minimax with Alpha-Beta Pruning

**Group Members:** Adnaan Deejay, Ryan McGough, Hai Sieu Cao

**Course:** CPSC 481 — Artificial Intelligence | California State University, Fullerton

## Overview

Connect Four is a strongly solved game with perfect play, the first player can always force a win. Rather than re-implementing standard Connect Four, this project extends it to support dynamic board sizes and configurable N values, moving into unsolved territory where the AI's heuristic evaluation function does real work.

The AI opponent supports adjustable difficulty levels and scales to any board size such as 8×8, 9×9, or beyond.

## Features

- Configurable board size (default 8×8, supports any dimensions)
- Configurable win condition
- Minimax search with Alpha-Beta Pruning
- Adjustable AI difficulty: controls search depth and blocking behavior
- Custom heuristic evaluation function (center control, threat detection, difficulty-scaled blocking)
- pygame GUI with hover preview and end-game messages
- Benchmark mode: pit two AI players against each other across any number of games

## Setup

```bash
pip install -r requirements.txt
python main.py
```

> **Note:** Requires Python 3.12. If on Python 3.14, run with `py -3.12 main.py`.

## Configuration

Edit `config.py` to change board size, win condition, AI difficulty, or benchmark parameters:

```python
# Board
ROWS      = 8   # Board height
COLS      = 8   # Board width
CONNECT_N = 4   # How many in a row to win

# AI
AI_DEPTH      = 5  # Minimax search depth — higher = stronger but slower
AI_DIFFICULTY = 2  # 1 = Easy, 2 = Medium, 3 = Hard

# Benchmark
BENCHMARK_P2_DEPTH      = 5   # Search depth for Player 2
BENCHMARK_P2_DIFFICULTY = 2   # Difficulty for Player 2
BENCHMARK_GAMES         = 20  # Number of games to run
BENCHMARK_WORKERS       = 4   # Parallel workers
```

## Running the Benchmark

To pit two AI players against each other:

```bash
python benchmark.py
```

Player 1 uses `AI_DIFFICULTY` and `AI_DEPTH`. Player 2 uses `BENCHMARK_P2_DIFFICULTY` and `BENCHMARK_P2_DEPTH`. Both are configurable in `config.py`.


## Project Structure

| File | Description |
|------|-------------|
| `config.py` | All configurable constants (board, AI, benchmark, UI settings) |
| `game.py` | Board logic, move validation, win detection (works for any board size/N) |
| `ai.py` | Minimax + alpha-beta pruning + difficulty scaled heuristic evaluation |
| `ui.py` | pygame interface — rendering, input handling |
| `main.py` | Entry point |
| `benchmark.py` | AI vs AI benchmark runner with multiprocessing |
| `requirements.txt` | Python dependencies |

## Algorithm

The AI uses Minimax with Alpha-Beta Pruning to search the game tree up to a configurable depth.

## Performance Evaluation

### Easy (depth 2) vs Hard (depth 5) — Variable Board Sizes

| Board | Trials | N | Easy Wins | Hard Wins |
|-------|--------|---|-----------|-----------|
| 7×6 (Standard) | 20 | 4 | 0 | 20 |
| 6×6 | 20 | 4 | 0 | 18 |
| 7×7 | 20 | 4 | 0 | 20 |
| 8×8 | 20 | 4 | 2 | 18 |

### Easy vs Hard — Variable Connect-N on 8×8 and 7×6

| Board | Trials | N | Easy Wins | Hard Wins |
|-------|--------|---|-----------|-----------|
| 8×8 | 20 | 4 | 1 | 19 |
| 8×8 | 20 | 5 | 0 | 20 |
| 8×8 | 20 | 6 | 0 | 20 |
| 7×6 (Standard) | 20 | 5 | 3 | 12 |

Hard AI dominates across all configurations. On larger boards and higher N values, the search space grows, the Easy AI occasionally benefits from increased complexity, while Hard maintains strong performance throughout.
