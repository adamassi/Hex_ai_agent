import unittest
from board import HexBoard

class TestHexWinCheck(unittest.TestCase):

    def test_no_win(self):
        board = HexBoard(3)
        # row, col, player
        board.make_move(0, 0, 1)
        board.make_move(0, 1, 2)
        self.assertFalse(board.check_win(1, 0, 0))
        self.assertFalse(board.check_win(2, 0, 1))
        # Display the board
        print("test_no_win")
        board.display()

    def test_player1_win_vertical(self):
        board = HexBoard(3)
        board.make_move(0, 0, 1)
        board.make_move(1, 0, 1)
        board.make_move(2, 0, 1)
        board.check_win(1, 2, 0)
        self.assertTrue(board.check_win(1, 2, 0))
        # Display the board
        print("test_player1_win_vertical")
        board.display()

    def test_player1_win_vertical_2(self):
        board = HexBoard(3)
        board.make_move(0, 0, 1)
        board.make_move(2, 0, 1)
        if(board.check_win(1, 2, 0) is False):
            print("should print")
        board.check_win(1, 2, 0)
        # Display the board
        print("test_player1_win_vertical 2")
        board.display()

    def test_player2_win_horizontal(self):
        board = HexBoard(3)
        board.make_move(0, 0, 2)
        board.make_move(0, 1, 2)
        board.make_move(0, 2, 2)
        self.assertTrue(board.check_win(2, 0, 2))
        # Display the board
        print("test_player2_win_horizontal")
        board.display()

    def test_mixed_moves_no_win(self):
        board = HexBoard(3)
        board.make_move(0, 0, 1)
        board.make_move(1, 0, 2)
        board.make_move(2, 0, 1)
        self.assertFalse(board.check_win(1, 2, 0))
        self.assertFalse(board.check_win(2, 1, 0))
        # Display the board
        print("test_mixed_moves_no_win")
        board.display()

if __name__ == '__main__':
    unittest.main()
