import unittest
from board import HexBoard

class TestCopyBoard(unittest.TestCase):
    """
    Unit tests for the copy_board method in the HexBoard class.
    """

    def test_copy_board_structure(self):
        """
        Test that the copied board has the same structure and state as the original board.
        """
        original_board = HexBoard(3)
        # Make some moves on the original board
        original_board.make_move(0, 0, 1)
        original_board.make_move(1, 1, 2)
        original_board.make_move(2, 2, 1)

        # Create a copy of the board
        copied_board = original_board.copy_board()

        print("Testing copy_board structure...first test")

        # Display the original board
        print("Original Board:")
        original_board.display()

        # Display the copied board
        print("Copied Board:")
        copied_board.display()

        # Assert that the copied board has the same size
        self.assertEqual(copied_board.size, original_board.size)

        # Assert that the states of all cells are the same
        for row in range(original_board.size):
            for col in range(original_board.size):
                self.assertEqual(
                    copied_board.board[row][col].get_cell_state(),
                    original_board.board[row][col].get_cell_state()
                )

    def test_independence_of_copied_board(self):
        """
        Test that modifying the original board does not affect the copied board.
        """
        print("////////////////////////////////////")
        original_board = HexBoard(3)
        # Make some moves on the original board
        original_board.make_move(0, 0, 1)
        original_board.make_move(1, 1, 2)

        # Create a copy of the board
        copied_board = original_board.copy_board()

        
        print("Testing independence of copied board...second test")
        print("before modification")
        print("Original Board:")
        original_board.display()
        print("Copied Board:")
        copied_board.display()

        # Modify the original board
        original_board.make_move(2, 2, 1)

        # Display the original board after modification
        print("Original Board After Modification: the original board should have changed")
        original_board.display()

        # Display the copied board
        print("Copied Board:")
        copied_board.display()

        # Assert that the copied board remains unchanged
        self.assertNotEqual(
            copied_board.board[2][2].get_cell_state(),
            original_board.board[2][2].get_cell_state()
        )

if __name__ == '__main__':
    unittest.main()