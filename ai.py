import math
import random
from game import (
    create_board, drop_piece, get_next_open_row,
    get_valid_locations, winning_move, is_terminal_node
)
from config import ROWS, COLS, CONNECT_N, EMPTY, HUMAN_PIECE, AI_PIECE, AI_DEPTH, AI_DIFFICULTY, BENCHMARK_P2_DEPTH


# ─── Evaluation Helpers ───────────────────────────────────────────

def score_window(window, piece, difficulty):
    """
    Score a single window (slice of CONNECT_N cells).

    Scoring logic:
      - CONNECT_N in a row            → very high reward
      - (CONNECT_N - 1) + 1 empty    → strong threat
      - (CONNECT_N - 2) + 2 empty    → mild opportunity
      - Opponent has (CONNECT_N - 1) → block urgently
    """
    opponent = HUMAN_PIECE if piece == AI_PIECE else AI_PIECE
    score = 0

    piece_count    = window.count(piece)
    empty_count    = window.count(EMPTY)
    opp_count      = window.count(opponent)

    if piece_count == CONNECT_N:
        score += 100
    elif piece_count == CONNECT_N - 1 and empty_count == 1:
        score += 10
    elif piece_count == CONNECT_N - 2 and empty_count == 2:
        score += 3

    if opp_count == CONNECT_N - 1 and empty_count == 1:
            # Difficulty scaling, AI is less inclined to block a winning move on lower difficulties. 
            score -= (20 * (difficulty)) + 20

    return score


def score_position(board, piece, difficulty):
    """
    Heuristic evaluation of the full board for the given piece.

    Components:
      1. Center column bonus  — center columns enable more winning lines
      2. Horizontal windows   — score every horizontal CONNECT_N-length slice
      3. Vertical windows     — score every vertical slice
      4. Both diagonal dirs   — score every diagonal slice
    """
    score = 0

    # 1. Center column preference
    center_col = COLS // 2
    center_array = [int(board[r][center_col]) for r in range(ROWS)]
    score += center_array.count(piece) * 4

    # For larger boards also reward the adjacent center columns
    if COLS > 7:
        for offset in [1, -1]:
            adj_col = center_col + offset
            if 0 <= adj_col < COLS:
                adj_array = [int(board[r][adj_col]) for r in range(ROWS)]
                score += adj_array.count(piece) * 2

    # 2. Horizontal
    for r in range(ROWS):
        row_array = [int(board[r][c]) for c in range(COLS)]
        for c in range(COLS - CONNECT_N + 1):
            window = row_array[c:c + CONNECT_N]
            score += score_window(window, piece, difficulty)

    # 3. Vertical
    for c in range(COLS):
        col_array = [int(board[r][c]) for r in range(ROWS)]
        for r in range(ROWS - CONNECT_N + 1):
            window = col_array[r:r + CONNECT_N]
            score += score_window(window, piece, difficulty)

    # 4. Diagonal (bottom-left → top-right)
    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLS - CONNECT_N + 1):
            window = [int(board[r + i][c + i]) for i in range(CONNECT_N)]
            score += score_window(window, piece, difficulty)

    # 5. Diagonal (top-left → bottom-right)
    for r in range(CONNECT_N - 1, ROWS):
        for c in range(COLS - CONNECT_N + 1):
            window = [int(board[r - i][c + i]) for i in range(CONNECT_N)]
            score += score_window(window, piece, difficulty)

    return score


# ─── Minimax with Alpha-Beta Pruning ─────────────────────────────

def minimax(board, depth, alpha, beta, maximizing_player, difficulty):
    """
    Minimax algorithm with alpha-beta pruning.

    Parameters
    ----------
    board              : current game board (numpy array)
    depth              : remaining search depth
    alpha              : best score the maximizer can guarantee so far
    beta               : best score the minimizer can guarantee so far
    maximizing_player  : True if it is the AI's turn

    Returns
    -------
    (best_col, best_score) — best column to play and its heuristic score
    """
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    # Base cases
    if terminal:
        if winning_move(board, AI_PIECE):
            return (None, 1_000_000)
        elif winning_move(board, HUMAN_PIECE):
            return (None, -1_000_000)
        else:  # Draw
            return (None, 0)

    if depth == 0:
        return (None, score_position(board, AI_PIECE, difficulty))

    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False, difficulty)[1]

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cut-off

        return best_col, value

    else:  # Minimizing player (human)
        value = math.inf
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, HUMAN_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True, difficulty)[1]

            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cut-off

        return best_col, value


def get_ai_move(board):
    """
    Top-level function to get the AI's chosen column.
    Calls minimax with full alpha-beta window.
    """

    # Odds of making a random move. Lower difficulty is more likely to make random "incorrect" moves.
    random_chance = max(0.0, 0.2 - (AI_DIFFICULTY * 0.15))

    if random_chance > 0 and random.random() < random_chance: 
        return random.choice(get_valid_locations(board))
    
    col, _ = minimax(board, AI_DEPTH, -math.inf, math.inf, True, AI_DIFFICULTY)
    return col


def get_ai_move_at_difficulty(board, piece, difficulty, depth):
    """
    Does the same thing as get_ai_move, but this is used for the benchmark only.
    Minimal change to ensure that there is no use of global variables, while
    still preserving the fundamental algorithm underneath.
    
    Flips the board perspective when called for HUMAN_PIECE so minimax
    searches from the maximizing player's point of view.
    """
    random_chance = max(0.0, 0.2 - (difficulty * 0.15))

    valid = get_valid_locations(board)

    if random_chance > 0 and random.random() < random_chance:
        return random.choice(valid)

    if piece == HUMAN_PIECE:
        search_board = board.copy()
        search_board[board == HUMAN_PIECE] = AI_PIECE
        search_board[board == AI_PIECE] = HUMAN_PIECE
    else:
        search_board = board

    col, _ = minimax(search_board, depth, -math.inf, math.inf, True, difficulty)
    return col if col is not None else random.choice(valid)