from board import HexBoard
from styles import get_move_by_style

def test_styles():
    board = HexBoard(5)

    # Simulate some moves
    board.make_move(2, 2, 1)
    board.make_move(1, 1, 1)
    board.make_move(3, 3, 2)

    board.display()

    legal_moves = board.get_legal_moves()
    # print("Legal moves:", legal_moves)
    current_player = 1

    for style in ["random", "center_bias", "aggressive", "defensive"]:
        move = get_move_by_style(board, current_player, legal_moves, style)
        print(f"Style '{style}' chose move: {move}")

if __name__ == "__main__":
    test_styles()
