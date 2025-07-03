# simulation.py

from styles import get_move_by_style
import random

def simulate_game_from_move(board, player, style, first_move):
    """
    Simulates a full game starting from `first_move` by `player`,
    using `style` for move selection. Returns the winner (1 or 2).
    """
    board_copy = board.copy_board()
    board_copy.make_move(*first_move, player)

    current_player = 3 - player  # Switch to opponent

    while True:
        legal_moves = board_copy.get_legal_moves()
        if not legal_moves:
            return 0  # draw (very rare in Hex)

        move = get_move_by_style(board_copy, current_player, legal_moves, style)
        board_copy.make_move(*move, current_player)

        if board_copy.winner != 0:
            return board_copy.winner

        current_player = 3 - current_player
