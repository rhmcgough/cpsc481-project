# ─── Board Settings ───────────────────────────────────────────────
ROWS = 8
COLS = 8
CONNECT_N = 4  # How many in a row to win (4 for standard, can increase for larger boards)

# ─── AI Settings ──────────────────────────────────────────────────
AI_DEPTH = 5  # Minimax search depth (increase for harder AI, decrease for speed)

# ─── Players ──────────────────────────────────────────────────────
HUMAN = 0
AI = 1

EMPTY = 0
HUMAN_PIECE = 1
AI_PIECE = 2

# ─── UI Settings (used by ui.py) ──────────────────────────────────
SQUARE_SIZE = 80
RADIUS = SQUARE_SIZE // 2 - 5

WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE  # +1 row for the piece-drop preview at top

BLUE   = (30,  80, 200)
BLACK  = (0,   0,   0)
RED    = (220, 50,  50)
YELLOW = (240, 200,  0)
WHITE  = (255, 255, 255)
GREY   = (40,  40,  40)
