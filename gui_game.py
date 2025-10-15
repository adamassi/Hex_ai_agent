import tkinter as tk
import math
from board import HexBoard
from agent import Agent

HEX_R = 28
MARGIN = 60

def hex_points(cx, cy):
    """Return the 6 vertices for a pointy-top hex centered at (cx, cy)."""
    pts = []
    for i in range(6):
        # pointy-top hex: start at -30° and step by 60°
        angle = math.radians(60 * i - 30)
        px = cx + HEX_R * math.cos(angle)
        py = cy + HEX_R * math.sin(angle)
        pts.append((px, py))
    return pts  # list of (x,y)

class HexGUI:
    def __init__(self, size=5, style="random", num_simulations=50, difficulty="medium"):
        # Game/config state
        self.size = size
        self.board = HexBoard(size)
        self.agent = Agent(player=1, style=style, num_simulations=num_simulations)
        self.current = 2  # Player 2 (human) starts

        # Compute canvas size large enough to hold hex grid + margins
        width = int(MARGIN * 2 + (size + size // 2) * math.sqrt(3) * HEX_R)
        height = int(MARGIN * 2 + size * 1.5 * HEX_R)

        # Tk root window and title reflecting style/difficulty
        self.root = tk.Tk()
        self.root.title(f"Hex {size}×{size} — Agent ({style}, {difficulty}) vs You")

        # Drawing surface
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack()

        # Handle mouse clicks on the canvas (for placing human stones)
        self.canvas.bind("<Button-1>", self.on_click)

        # Status text at top-left
        self.status = self.canvas.create_text(
            10, 10, anchor="nw",
            text="Your turn! (Blue, Player 2)",
            font=("Arial", 14), fill="black"
        )

        # Map from polygon id -> (row, col) to resolve clicks to cells
        self.hex_index = {}

        # Initial draw
        self.draw_board()

        # Simple Quit button
        quit_btn = tk.Button(
            self.root,
            text="Quit",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#e74c3c",
            activebackground="#f2f2f2",
            activeforeground="#c0392b",
            width=8,
            relief="raised",
            bd=4,
            cursor="hand2",
            command=self.root.destroy
        )
        quit_btn.pack(pady=(8, 10))

    def hex_center(self, row, col):
        """Compute pixel center (x,y) of hex at grid (row, col)."""
        dx = math.sqrt(3) * HEX_R      # horizontal spacing between columns
        dy = 1.5 * HEX_R               # vertical spacing between rows
        x = MARGIN + col * dx + row * (dx / 2)  # staggered columns
        y = MARGIN + row * dy
        return x, y

    def draw_board(self):
        """Redraw all hexes and colored edge bands based on board state."""
        # Clear previous drawings
        self.canvas.delete("hex")
        self.canvas.delete("edges")
        self.hex_index = {}

        # Draw cells (stones and empty)
        for r in range(self.size):
            for c in range(self.size):
                cx, cy = self.hex_center(r, c)
                pts = hex_points(cx, cy)
                flat_pts = [coord for p in pts for coord in p]

                state = self.board.board[r][c].get_cell_state()

                # Default empty colors
                fill = "white"
                outline = "black"

                # Red (player 1) / Blue (player 2)
                if state == 1:
                    fill = "#e74c3c"
                elif state == 2:
                    fill = "#3498db"

                poly_id = self.canvas.create_polygon(
                    flat_pts, fill=fill, outline=outline, width=2, tags="hex"
                )
                self.hex_index[poly_id] = (r, c)

        # Draw colored edge bands indicating connection goals
        edge_width = 5

        # Top border (red)
        top_points = []
        for c in range(self.size):
            cx, cy = self.hex_center(0, c)
            pts = hex_points(cx, cy)
            if c == 0:
                top_points.append(pts[4])
            top_points.append(pts[5])
            top_points.append(pts[0])
        self.canvas.create_line(top_points, fill="#e74c3c", width=edge_width, tags="edges")

        # Bottom border (red)
        bottom_points = []
        for c in range(self.size):
            cx, cy = self.hex_center(self.size - 1, c)
            pts = hex_points(cx, cy)
            bottom_points.append(pts[3])
            bottom_points.append(pts[2])
        bottom_points.append(pts[1])
        self.canvas.create_line(bottom_points, fill="#e74c3c", width=edge_width, tags="edges")

        # Left border (blue)
        left_points = []
        for r in range(self.size):
            cx, cy = self.hex_center(r, 0)
            pts = hex_points(cx, cy)
            left_points.append(pts[4])
            left_points.append(pts[3])
        self.canvas.create_line(left_points, fill="#3498db", width=edge_width, tags="edges")

        # Right border (blue)
        right_points = []
        for r in range(self.size):
            cx, cy = self.hex_center(r, self.size - 1)
            pts = hex_points(cx, cy)
            right_points.append(pts[0])
            right_points.append(pts[1])
        self.canvas.create_line(right_points, fill="#3498db", width=edge_width, tags="edges")

    def on_click(self, event):
        """Handle human click; place a blue stone if valid and trigger agent."""
        # Ignore clicks after game end or when not human's turn
        if self.board.winner != 0 or self.current != 2:
            return

        # Find topmost polygon (hex) under the cursor
        ids = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        hex_id = None
        for iid in reversed(ids):
            if "hex" in self.canvas.gettags(iid):
                hex_id = iid
                break
        if hex_id is None:
            return

        r, c = self.hex_index.get(hex_id, (None, None))
        if r is None:
            return

        # If move is valid, switch to agent's turn
        if self.board.make_move(r, c, 2):
            self.current = 1
            self.after_move()

    def after_move(self):
        """Post-human-move hook: redraw, check win, schedule agent turn."""
        self.draw_board()

        # If someone won after human move, show and stop
        if self.board.winner != 0:
            self.show_winner()
            return

        # Agent's turn: update status and schedule agent computation shortly
        if self.current == 1:
            self.canvas.itemconfig(self.status, text="Agent is thinking...")
            self.canvas.update_idletasks()  # Ensure UI refresh before thinking

            # Schedule agent move; do not block UI thread
            self.root.after(200, self.agent_turn)

            # NOTE: removed stale code that referenced undefined 'move' and duplicated logic

    def agent_turn(self):
        """Run the agent's move after UI has refreshed."""
        move = self.agent.choose_move(self.board)
        if move:
            self.board.make_move(*move, 1)

        # Hand turn back to the human
        self.current = 2
        self.draw_board()

        # Check for end of game and update status
        if self.board.winner != 0:
            self.show_winner()
        else:
            self.canvas.itemconfig(self.status, text="Your turn! (Blue, Player 2)")

    def show_winner(self):
        """Update status banner to announce the winner."""
        if self.board.winner == 1:
            msg = "🏆 Agent (Red) wins!"
        elif self.board.winner == 2:
            msg = "🏆 You (Blue) win!"
        else:
            msg = "It's a draw."
        self.canvas.itemconfig(self.status, text=msg, fill="green")

    def run(self):
        """Enter Tk main loop."""
        self.root.mainloop()

# --- Launcher (lets the user pick size, style, difficulty) ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hex Game Setup")
    # Let Tk size to fit contents, but ensure minimum height so all options show
    root.minsize(360, 420)
    root.resizable(False, False)
    root.configure(bg="#f2f2f2")

    # Title
    tk.Label(
        root,
        text="HEX GAME",
        font=("Helvetica", 18, "bold"),
        fg="#d90429",
        bg="#f2f2f2",
    ).pack(pady=(20, 10))

    # Board size dropdown
    tk.Label(root, text="Board Size", font=("Helvetica", 13, "bold"), bg="#f2f2f2").pack(pady=(5, 3))
    size_var = tk.StringVar(value="5")
    size_options = [str(n) for n in (3, 5, 7, 9, 11, 13)]
    size_menu = tk.OptionMenu(root, size_var, *size_options)
    size_menu.config(width=12, font=("Helvetica", 12))
    size_menu.pack(pady=6)

    # Agent style dropdown
    tk.Label(root, text="Agent Play Style", font=("Helvetica", 13, "bold"), bg="#f2f2f2").pack(pady=(10, 3))
    style_var = tk.StringVar(value="random")
    style_options = ["random", "center_bias", "defensive", "aggressive"]
    style_menu = tk.OptionMenu(root, style_var, *style_options)
    style_menu.config(width=14, font=("Helvetica", 12))
    style_menu.pack(pady=6)

    # Difficulty dropdown -> maps to agent Monte Carlo simulations
    tk.Label(root, text="Difficulty", font=("Helvetica", 13, "bold"), bg="#f2f2f2").pack(pady=(10, 3))
    difficulty_var = tk.StringVar(value="medium")
    difficulty_options = ["easy", "medium", "hard"]
    difficulty_menu = tk.OptionMenu(root, difficulty_var, *difficulty_options)
    difficulty_menu.config(width=14, font=("Helvetica", 12))
    difficulty_menu.pack(pady=6)

    # Start button handler: build HexGUI with chosen settings
    def start_game():
        size = int(size_var.get())
        style = style_var.get()
        difficulty = difficulty_var.get().lower()

        # Map difficulty to number of Monte Carlo rollouts
        difficulty_to_sims = {"easy": 5, "medium": 80, "hard": 200}
        num_sims = difficulty_to_sims.get(difficulty, 80)

        root.destroy()
        app = HexGUI(size=size, style=style, num_simulations=num_sims, difficulty=difficulty)
        app.run()

    # Start button
    start_btn = tk.Button(
        root,
        text="▶  Start Game",
        command=start_game,
        font=("Helvetica", 15, "bold"),
        width=16,
        bg="#1f7ae0",
        fg="black",
        activebackground="#1557a0",
        activeforeground="black",
        relief="raised",
        bd=5,
        cursor="hand2",
        pady=8,
    )
    start_btn.pack(pady=(25, 16))

    # Simple hover effect
    def on_enter(e): start_btn.config(bg="#4d9fff")
    def on_leave(e): start_btn.config(bg="#1f7ae0")
    start_btn.bind("<Enter>", on_enter)
    start_btn.bind("<Leave>", on_leave)

    root.mainloop()
