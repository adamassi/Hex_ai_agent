import unittest
from board import HexBoard

class TestHexWinCheck(unittest.TestCase):
    """
    Unit tests for the HexBoard class to check win conditions.
    """

    def test_no_win(self):
        """
        Test case where no player has won yet.
        """
        board = HexBoard(3)
        # Player 1 makes a move at (0, 0)
        board.make_move(0, 0, 1)
        # Player 2 makes a move at (0, 1)
        board.make_move(0, 1, 2)
        # Assert that neither player has won
        self.assertFalse(board.check_win(1, 0, 0))
        self.assertFalse(board.check_win(2, 0, 1))
        # Display the board
        print("test_no_win")
        board.display()

    def test_player1_win_vertical(self):
        """
        Test case where Player 1 wins by connecting top to bottom vertically.
        """
        board = HexBoard(3)
        # Player 1 makes moves to connect vertically
        board.make_move(0, 0, 1)
        board.make_move(1, 0, 1)
        board.make_move(2, 0, 1)
        # Assert that Player 1 has won
        self.assertTrue(board.check_win(1, 2, 0))
        # Display the board
        print("test_player1_win_vertical")
        board.display()

    def test_player2_win_horizontal(self):
        """
        Test case where Player 2 wins by connecting left to right horizontally.
        """
        board = HexBoard(3)
        # Player 2 makes moves to connect horizontally
        board.make_move(0, 0, 2)
        board.make_move(0, 1, 2)
        board.make_move(0, 2, 2)
        # Assert that Player 2 has won
        self.assertTrue(board.check_win(2, 0, 2))
        # Display the board
        print("test_player2_win_horizontal")
        board.display()

    def test_mixed_moves_no_win(self):
        """
        Test case where mixed moves are made, but no player has won.
        """
        board = HexBoard(3)
        # Mixed moves by Player 1 and Player 2
        board.make_move(0, 0, 1)
        board.make_move(1, 0, 2)
        board.make_move(2, 0, 1)
        # Assert that neither player has won
        self.assertFalse(board.check_win(1, 2, 0))
        self.assertFalse(board.check_win(2, 1, 0))
        # Display the board
        print("test_mixed_moves_no_win")
        board.display()

if __name__ == '__main__':
    unittest.main()
