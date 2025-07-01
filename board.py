from union_find import union , find
import copy

"""
player 1 is represented by 1, player 2 by 2, and empty cells by 0.
1 is the read player:play  from top to down,
2 is the blue player:play from lift to right.
"""


class Cell:
    def __init__(self, row, col):
        """Initialize a cell with its row, column, state, neighbors, and Union-Find pointers."""
        self.row = row
        self.col = col
        self.state = 0  # 0 = empty, 1 = player 1, 2 = player 2
        self.neighbors = []  # List of neighboring cells
        self.parent = self  # Union-Find: parent pointer (initially points to itself)
        self.rank = 1       # Union-Find: rank for union by rank optimization

        self.touch_top = False
        self.touch_bottom = False
        self.touch_left = False
        self.touch_right = False


    def get_location(self):
        """Returns the location of the cell as a tuple (row, col)."""
        return self.row, self.col

    def get_cell_state(self):
        """Returns the state of the cell: 0 = empty, 1 = player 1, 2 = player 2."""
        return self.state

    def set_cell_state(self, new_state):
        """
        Sets the state of the cell and performs union with neighbors of the same state.
        If the new state matches the state of a neighbor, the cells are united.
        """
        if new_state in [1, 2]:  # Ensure the state is valid (1 or 2)
            self.state = new_state
            # Iterate over neighbors and perform union if states match
            for neighbor in self.neighbors:
                if neighbor.get_cell_state() == new_state:
                    union(self, neighbor)  # Union the current cell with the neighbor
        else:
            raise ValueError("Invalid state. Use 0 (empty), 1 (player 1), or 2 (player 2).")

    def add_neighbor(self, neighbor_cell):
        """
        Adds a neighbor relationship to both cells (undirected connection).
        Ensures that the neighbor is added to both cells' neighbor lists.
        """
        if neighbor_cell not in self.neighbors:
            self.neighbors.append(neighbor_cell)
        if self not in neighbor_cell.neighbors:
            neighbor_cell.neighbors.append(self)

    def get_neighbors(self):
        """Returns a list of neighboring cells."""
        return self.neighbors


class HexBoard:
    def __init__(self, size):
        """Initialize a HexBoard with the given size and create the board."""
        self.size = size  # Size of the board (size x size)
        self.board = [[Cell(row, col) for col in range(self.size)] for row in range(self.size)]
        self.make_board()  # Connect neighbors in the hex grid
        self.wineer = 0

    def make_board(self):
        """
        Fills the board with Cell objects and connects neighbors in a hex grid.
        Each cell is connected to its valid neighbors based on hex grid rules.
        """
        for row in range(self.size):
            for col in range(self.size):
                current = self.board[row][col]
                if row == 0:
                    current.touch_top = True
                if row == self.size - 1:
                    current.touch_bottom = True
                if col == 0:
                    current.touch_left = True
                if col == self.size - 1:
                    current.touch_right = True
                # 6 possible neighbor directions in a hex grid
                neighbor_coords = [
                    (row - 1, col),     # Up
                    (row - 1, col + 1), # Up-right
                    (row, col - 1),     # Left
                    (row, col + 1),     # Right
                    (row + 1, col - 1), # Down-left
                    (row + 1, col)      # Down
                ]
                # Add valid neighbors to the current cell
                for r, c in neighbor_coords:
                    if 0 <= r < self.size and 0 <= c < self.size:  # Check bounds
                        neighbor = self.board[r][c]
                        current.add_neighbor(neighbor)

    def is_valid_move(self, row, col):
        """
        Checks if a move is valid.
        A move is valid if the cell is within bounds and is currently empty.
        """
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col].get_cell_state() == 0

    def make_move(self, row, col, player):
        """
        Makes a move for the given player at the specified row and column.
        Returns True if the move is successful, False otherwise.
        """
        if self.is_valid_move(row, col):
            self.board[row][col].set_cell_state(player)  # Set the cell state to the player's state
            # Check if the player has won after making the move
            if self.check_win(player, row, col):
                self.winner = player
            return True
        return False

    def check_win(self, player, row, col):
        """
        Checks if the given player has won the game.
        if the parint of the cell is the is another edge of the board
        """
        root = find(self.board[row][col])
        # Check if the root component connects the player's respective sides
        if player == 1 and root.touch_top and root.touch_bottom:
            return True
        elif player == 2 and root.touch_left and root.touch_right:
            return True

        return False

    def copy_board(self):
        """
        Returns a deep copy of the current HexBoard.
        """
        new_board = HexBoard(self.size)
        for row in range(self.size):
            for col in range(self.size):
                current_cell = self.board[row][col]
                copied_cell = new_board.board[row][col]
                copied_cell.state = current_cell.state
                copied_cell.touch_top = current_cell.touch_top
                copied_cell.touch_bottom = current_cell.touch_bottom
                copied_cell.touch_left = current_cell.touch_left
                copied_cell.touch_right = current_cell.touch_right
                copied_cell.rank = current_cell.rank
                
                # Deep copy the parent pointer
                copied_cell.parent = new_board.board[current_cell.parent.row][current_cell.parent.col]
        return new_board

    def display(self):
        """
        Displays the board in a hexagonal structure.
        Empty cells are represented by '.', Player 1's cells by 'X', and Player 2's cells by 'O'.
        """
        for row in range(self.size):
            print(" " * row, end="")  # Offset for hex structure
            for col in range(self.size):
                cell_state = self.board[row][col].get_cell_state()
                symbol = "." if cell_state == 0 else ("X" if cell_state == 1 else "O")
                print(symbol, end=" ")
            print()
