from board import HexBoard

def test_board_display():
    # Create a HexBoard of size 5x5
    size = 5
    board = HexBoard(size)

    # Make some moves
    board.make_move(0, 0, 1)  # Player 1
    board.make_move(1, 1, 2)  # Player 2
    board.make_move(2, 2, 1)  # Player 1
    board.make_move(3, 3, 2)  # Player 2

    # Display the board
    print("Hex Board Display:")
    board.display()

if __name__ == "__main__":
    test_board_display()