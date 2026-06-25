"""
benchmark.py — Pit two AI players against each other.
Usage: python benchmark.py
Player1 (HUMAN_PIECE) uses BENCHMARK_HUMAN_DIFFICULTY from config.py
Player2 (AI_PIECE)    uses AI_DIFFICULTY from config.py

Note that HUMAN refers to an AI Player 1.
"""
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from game import create_board, drop_piece, get_next_open_row, get_valid_locations, winning_move, is_terminal_node
from ai import get_ai_move_at_difficulty
from config import (
    HUMAN_PIECE, AI_PIECE,
    AI_DIFFICULTY,
    BENCHMARK_P2_DIFFICULTY, BENCHMARK_GAMES, BENCHMARK_WORKERS,
    AI_DEPTH, BENCHMARK_P2_DEPTH,
    ROWS, COLS, CONNECT_N
)
 
 

def play_game(difficulty_1, depth_1, difficulty_2, depth_2, first_player=AI_PIECE):
    """
    Play one game between two AI players at given difficulties.
    Returns the winning piece (HUMAN_PIECE / AI_PIECE) or None for a draw.
    difficulty_1 controls HUMAN_PIECE, difficulty_2 controls AI_PIECE.
    """
    board = create_board()
    turn = first_player
 
    while not is_terminal_node(board):
        valid = get_valid_locations(board)
        if not valid:
            break
 
        if turn == HUMAN_PIECE:
            col = get_ai_move_at_difficulty(board, HUMAN_PIECE, difficulty_1, depth_1)
        else:
            col = get_ai_move_at_difficulty(board, AI_PIECE, difficulty_2, depth_2)
 
        if col is None or col not in valid:
            col = random.choice(valid)
 
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, turn)
 
        if winning_move(board, turn):
            return turn
 
        turn = AI_PIECE if turn == HUMAN_PIECE else HUMAN_PIECE

    # Draw
    return None
 
 
def run_benchmark():
    # these parameters can be changed in config.py
    difficulty_1 = AI_DIFFICULTY            # normal AI opponent
    difficulty_2 = BENCHMARK_P2_DIFFICULTY  # AI simulating the human (P2)
    n_games      = BENCHMARK_GAMES
    max_workers  = BENCHMARK_WORKERS
    depth_1      = AI_DEPTH
    depth_2      = BENCHMARK_P2_DEPTH
 
    results = {HUMAN_PIECE: 0, AI_PIECE: 0, None: 0}
 
    # multithreading to speed up benchmarking.
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(play_game, difficulty_1, depth_1, difficulty_2, depth_2, HUMAN_PIECE)
            for _ in range(n_games)
        ]
        for future in as_completed(futures):
            results[future.result()] += 1
 
    print(f"\nBenchmark: P1 (difficulty={difficulty_1}, depth={AI_DEPTH}) vs P2 (difficulty={difficulty_2}, depth={BENCHMARK_P2_DEPTH}), {n_games} games, {ROWS} rows x {COLS} columns, Connect-{CONNECT_N} to win.")
    print(f"  P1 wins: {results[HUMAN_PIECE]}")
    print(f"  P2 wins: {results[AI_PIECE]}")
    print(f"  Draws:   {results[None]}")
    print(f"  To change benchmark values, edit the parameters in config.py")
 
 
if __name__ == "__main__":
    run_benchmark()