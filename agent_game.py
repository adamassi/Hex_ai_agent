# agent_game.py
from board import HexBoard
from agent import Agent

def parse_coord(s, size):
    """Parse human input into (row, col) coordinates (0-based)."""
    s = s.strip()
    if not s:
        return None
    parts = s.split()
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        r, c = int(parts[0]) - 1, int(parts[1]) - 1
        if 0 <= r < size and 0 <= c < size:
            return (r, c)
    if len(s) >= 2 and s[0].isalpha():
        col = ord(s[0].upper()) - ord('A')
        row = int(s[1:]) - 1
        if 0 <= row < size and 0 <= col < size:
            return (row, col)
    return None

def prompt_human(size):
    """Ask the human player for a move."""
    while True:
        s = input(f"Your move (row col or A1, q=quit): ").strip()
        if s.lower() in ("q", "quit", "exit"):
            return None
        mv = parse_coord(s, size)
        if mv is not None:
            return mv
        print("Invalid input. Try again.")

def play_game(size=5, style="random", num_simulations=100):
    board = HexBoard(size)
    agent = Agent(player=1, style=style, num_simulations=num_simulations)

    print(f"\nStarting Hex! Size {size}x{size}")
    board.display()
    print("Player 1 = Agent (X, top-bottom)\nPlayer 2 = You (O, left-right)\n")

    current = 1
    while True:
        if current == 1:
            print("\nAgent is thinking...")
            move = agent.choose_move(board)
            if move is None:
                print("Agent has no moves. Game over.")
                break
            board.make_move(move[0], move[1], 1)
            print(f"Agent plays {move}")
        else:
            print("\nYour turn!")
            move = prompt_human(size)
            if move is None:
                print("You quit the game.")
                break
            if not board.make_move(move[0], move[1], 2):
                print("That move is not valid. Try again.")
                continue

        board.display()

        if board.winner != 0:
            if board.winner == 1:
                print("\n🏆 Agent wins!")
            else:
                print("\n🏆 You win!")
            break

        current = 2 if current == 1 else 1

if __name__ == "__main__":
    try:
        size = int(input("Enter board size (default 5): ") or 5)
    except ValueError:
        size = 5
    play_game(size=size, style="random", num_simulations=50)
