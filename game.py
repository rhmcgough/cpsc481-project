import numpy as np
from config import ROWS, COLS, CONNECT_N, EMPTY, HUMAN_PIECE, AI_PIECE


def create_board():
    """Create an empty ROWS x COLS board."""
    return np.zeros((ROWS, COLS), dtype=int)


def drop_piece(board, row, col, piece):
    """Place a piece on the board at (row, col)."""
    board[row][col] = piece


def is_valid_location(board, col):
    """A column is valid if the top cell is still empty."""
    return board[ROWS - 1][col] == EMPTY


def get_next_open_row(board, col):
    """Return the lowest empty row in a given column."""
    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r
    return None


def get_valid_locations(board):
    """Return all columns that can still accept a piece."""
    return [c for c in range(COLS) if is_valid_location(board, c)]


def winning_move(board, piece):
    """
    Check if the given piece has achieved CONNECT_N in a row
    in any direction (horizontal, vertical, diagonal).
    Works for any board size and any CONNECT_N value.
    """
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - CONNECT_N + 1):
            if all(board[r][c + i] == piece for i in range(CONNECT_N)):
                return True

    # Vertical
    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(CONNECT_N)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLS - CONNECT_N + 1):
            if all(board[r + i][c + i] == piece for i in range(CONNECT_N)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(CONNECT_N - 1, ROWS):
        for c in range(COLS - CONNECT_N + 1):
            if all(board[r - i][c + i] == piece for i in range(CONNECT_N)):
                return True

    return False


def is_terminal_node(board):
    """Return True if the game is over (win or draw)."""
    return (
        winning_move(board, HUMAN_PIECE)
        or winning_move(board, AI_PIECE)
        or len(get_valid_locations(board)) == 0
    )


def print_board(board):
    """Print the board flipped so row 0 appears at the bottom."""
    print(np.flip(board, 0))
