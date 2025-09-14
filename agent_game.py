# agent_game.py
from board import HexBoard
from agent import Agent

def parse_coord(s, size):
    """
    Parse human input into (row, col) coordinates (0-based).
    - Accepts input in the format "row col" (e.g., "2 3").
    - Accepts input in the format "A1" (column letter + row number).
    Returns a tuple (row, col) or None if the input is invalid.
    """
    s = s.strip()
    if not s:
        return None
    # Try "row col" format
    parts = s.split()
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        r, c = int(parts[0]) - 1, int(parts[1]) - 1
        if 0 <= r < size and 0 <= c < size:
            return (r, c)
    # Try "A1" format
    if len(s) >= 2 and s[0].isalpha():
        col = ord(s[0].upper()) - ord('A')
        row = int(s[1:]) - 1
        if 0 <= row < size and 0 <= col < size:
            return (row, col)
    return None

def prompt_human(size):
    """
    Prompt the human player for a move.
    - Repeatedly asks for input until a valid move is provided.
    - Returns the move as a tuple (row, col) or None if the player quits.
    """
    while True:
        s = input(f"Your move (row col or A1, q=quit): ").strip()
        if s.lower() in ("q", "quit", "exit"):
            return None  # Player chose to quit
        mv = parse_coord(s, size)
        if mv is not None:
            return mv  # Valid move
        print("Invalid input. Try again.")  # Invalid input, prompt again

def play_game(size=5, style="random", num_simulations=100):
    """
    Play a game of Hex between an agent and a human player.
    - The agent plays as Player 1 (X, top-bottom).
    - The human plays as Player 2 (O, left-right).
    - The game continues until there is a winner or the player quits.
    """
    board = HexBoard(size)  # Initialize the Hex board
    agent = Agent(player=1, style=style, num_simulations=num_simulations)  # Initialize the agent

    print(f"\nStarting Hex! Size {size}x{size}")
    board.display()
    print("Player 1 = Agent (X, top-bottom)\nPlayer 2 = You (O, left-right)\n")

    current = 1  # Player 1 (Agent) starts
    while True:
        if current == 1:
            print("\nAgent is thinking...")
            move = agent.choose_move(board)  # Agent chooses a move
            if move is None:
                print("Agent has no moves. Game over.")
                break
            board.make_move(move[0], move[1], 1)  # Agent makes the move
            print(f"Agent plays {move}")
        else:
            print("\nYour turn!")
            move = prompt_human(size)  # Prompt the human for a move
            if move is None:
                print("You quit the game.")
                break
            if not board.make_move(move[0], move[1], 2):  # Validate and make the move
                print("That move is not valid. Try again.")
                continue

        board.display()  # Display the board after each move

        # Check if there is a winner
        if board.winner != 0:
            if board.winner == 1:
                print("\n🏆 Agent wins!")
            else:
                print("\n🏆 You win!")
            break

        # Switch to the other player
        current = 2 if current == 1 else 1

if __name__ == "__main__":
    try:
        # Prompt the user for the board size, default to 5 if input is invalid
        size = int(input("Enter board size (default 5): ") or 5)
    except ValueError:
        size = 5
    play_game(size=size, style="random", num_simulations=50)
