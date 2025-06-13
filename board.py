from union_find import union

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = 0  # 0 = empty, 1 = player 1, 2 = player 2
        self.neighbors = []
        self.parent = self  # Union-Find: parent pointer
        self.rank = 0       # Union-Find: rank

    def get_location(self):
        """Returns location of cell as (row, col)"""
        return self.row, self.col

    def get_cell_state(self):
        """Returns state of cell: 0 = empty, 1 = player 1, 2 = player 2"""
        return self.state

    def set_cell_state(self, new_state):
        """Sets the state of the cell and performs union with neighbors of the same state"""
        if new_state in [0, 1, 2]:
            self.state = new_state
            # Iterate over neighbors and perform union if states match
            for neighbor in self.neighbors:
                if neighbor.get_cell_state() == new_state:
                    union(self, neighbor)
        else:
            raise ValueError("Invalid state. Use 0 (empty), 1 (player 1), or 2 (player 2).")
        

    def add_neighbor(self, neighbor_cell):
        """Adds a neighbor relationship to both cells (undirected connection)"""
        if neighbor_cell not in self.neighbors:
            self.neighbors.append(neighbor_cell)
        if self not in neighbor_cell.neighbors:
            neighbor_cell.neighbors.append(self)

    def get_neighbors(self):
        """Returns list of neighbor cells"""
        return self.neighbors


class HexBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[Cell(row, col) for col in range(self.size)] for row in range(self.size)]
        self.make_board()

    def make_board(self):
        """Fills board with Cell objects and connects neighbors in a hex grid"""
        for row in range(self.size):
            for col in range(self.size):
                current = self.board[row][col]
                # 6 possible neighbor directions in a hex grid
                neighbor_coords = [
                    (row - 1, col),     # Up
                    (row - 1, col + 1), # Up-right
                    (row, col - 1),     # Left
                    (row, col + 1),     # Right
                    (row + 1, col - 1), # Down-left
                    (row + 1, col)      # Down
                ]
                for r, c in neighbor_coords:
                    if 0 <= r < self.size and 0 <= c < self.size:
                        neighbor = self.board[r][c]
                        current.add_neighbor(neighbor)

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col].get_cell_state() == 0

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col].set_cell_state(player)
            return True
        return False

    def check_win(self, player):
        # Placeholder for DFS or Union-Find implementation
        pass

    def display(self):
        for row in range(self.size):
            print(" " * row, end="")  # Offset for hex structure
            for col in range(self.size):
                cell_state = self.board[row][col].get_cell_state()
                symbol = "." if cell_state == 0 else ("X" if cell_state == 1 else "O")
                print(symbol, end=" ")
            print()
