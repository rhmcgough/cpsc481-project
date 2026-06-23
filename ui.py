"""
ui.py — pygame UI for Connect Four AI
======================================
Owned by: [Third Member]

This file handles all rendering and user input.
The game logic lives in game.py and the AI lives in ai.py.
"""

import sys
import pygame
from game import (
    create_board, drop_piece, get_next_open_row,
    get_valid_locations, winning_move, is_terminal_node, print_board
)
from ai import get_ai_move
from config import (
    ROWS, COLS, CONNECT_N,
    HUMAN, AI, HUMAN_PIECE, AI_PIECE, EMPTY,
    SQUARE_SIZE, RADIUS, WIDTH, HEIGHT,
    BLUE, BLACK, RED, YELLOW, WHITE, GREY
)


def draw_board(board, screen):
    """Render the board grid and all placed pieces."""
    for c in range(COLS):
        for r in range(ROWS):
            # Draw blue grid cell
            pygame.draw.rect(
                screen, BLUE,
                (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            # Draw circle (piece or empty hole)
            piece = board[ROWS - 1 - r][c]
            color = BLACK if piece == EMPTY else (RED if piece == HUMAN_PIECE else YELLOW)
            pygame.draw.circle(
                screen, color,
                (c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                RADIUS
            )
    pygame.display.update()


def draw_preview(col, turn, screen):
    """Draw the hovering piece at the top of the column."""
    pygame.draw.rect(screen, GREY, (0, 0, WIDTH, SQUARE_SIZE))
    if turn == HUMAN:
        pygame.draw.circle(
            screen, RED,
            (col * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2),
            RADIUS
        )
    pygame.display.update()


def show_message(text, color, screen, font):
    """Display a centered end-game message."""
    label = font.render(text, True, color)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 10))
    pygame.display.update()


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Connect {CONNECT_N} — {ROWS}x{COLS}")

    font = pygame.font.SysFont("monospace", 60, bold=True)
    small_font = pygame.font.SysFont("monospace", 30)

    board = create_board()
    print_board(board)
    draw_board(board, screen)

    turn = HUMAN  # Human goes first
    game_over = False
    hover_col = COLS // 2

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # ── Mouse hover preview ──────────────────────────────
            if event.type == pygame.MOUSEMOTION and turn == HUMAN:
                hover_col = event.pos[0] // SQUARE_SIZE
                hover_col = max(0, min(hover_col, COLS - 1))
                draw_preview(hover_col, turn, screen)

            # ── Human click ─────────────────────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and turn == HUMAN:
                col = event.pos[0] // SQUARE_SIZE
                col = max(0, min(col, COLS - 1))

                if col in get_valid_locations(board):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, HUMAN_PIECE)
                    print_board(board)

                    if winning_move(board, HUMAN_PIECE):
                        draw_board(board, screen)
                        show_message("You win! 🎉", RED, screen, font)
                        game_over = True
                    elif not get_valid_locations(board):
                        draw_board(board, screen)
                        show_message("Draw!", WHITE, screen, font)
                        game_over = True
                    else:
                        turn = AI
                        draw_board(board, screen)

        # ── AI turn ─────────────────────────────────────────────
        if turn == AI and not game_over:
            pygame.draw.rect(screen, GREY, (0, 0, WIDTH, SQUARE_SIZE))
            thinking = small_font.render("AI thinking...", True, YELLOW)
            screen.blit(thinking, (10, 10))
            pygame.display.update()

            col = get_ai_move(board)

            if col is not None and col in get_valid_locations(board):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                print_board(board)

                if winning_move(board, AI_PIECE):
                    draw_board(board, screen)
                    show_message("AI wins!", YELLOW, screen, font)
                    game_over = True
                elif not get_valid_locations(board):
                    draw_board(board, screen)
                    show_message("Draw!", WHITE, screen, font)
                    game_over = True
                else:
                    turn = HUMAN
                    draw_board(board, screen)

        if game_over:
            pygame.time.wait(3000)

        clock.tick(30)
