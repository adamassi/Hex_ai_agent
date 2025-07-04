# simulation.py

from styles import get_move_by_style
import random

def simulate_game_from_move(board, player, style, first_move):
    """
    Simulates a full game starting from `first_move` by `player`,
    using `style` for move selection. Returns the winner (1 or 2).
    """
    # Create a deep copy of the board to simulate the game without altering the original board
    board_copy = board.copy_board()
    
    # Make the first move for the given player
    board_copy.make_move(*first_move, player)

    # Initialize the current player to the opponent (3 - player toggles between 1 and 2)
    current_player = 3 - player

    while True:
        # Get all legal moves for the current player
        legal_moves = board_copy.get_legal_moves()
        
        # If there are no legal moves, the game ends in a draw (rare in Hex)
        if not legal_moves:
            return 0  # draw

        # Select a move based on the specified style
        move = get_move_by_style(board_copy, current_player, legal_moves, style)
        
        # Make the selected move for the current player
        board_copy.make_move(*move, current_player)

        # Check if the current player has won the game
        if board_copy.winner != 0:
            return board_copy.winner  # Return the winner (1 or 2)

        # Switch to the other player for the next turn
        current_player = 3 - current_player
