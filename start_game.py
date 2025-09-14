#!/usr/bin/env python3
"""
start_game.py — Interactive Hex game (two humans in terminal).

- Uses your HexBoard from board.py
- Continues until there is a winner
- EACH ROUND asks the *current* player for their move
- Accepts input as "row col" (1-based) or like "B3" (column letter + 1-based row)

Players:
  Player 1 = 'X' (connects TOP to BOTTOM)
  Player 2 = 'O' (connects LEFT to RIGHT)

Run:
  python start_game.py --size 5
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional, Tuple

from board import HexBoard  # relies on your existing implementation


def parse_coord(s: str, size: int) -> Optional[Tuple[int, int]]:
    """
    Parse a coordinate input.
    - 'row col' (1-based), e.g. '2 3'
    - 'B3' (col letter then 1-based row), case-insensitive
    Returns (row, col) as 0-based indices, or None if invalid.
    """
    s = s.strip()
    if not s:
        return None

    # Try "row col"
    parts = s.split()
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        r = int(parts[0]) - 1
        c = int(parts[1]) - 1
        if 0 <= r < size and 0 <= c < size:
            return (r, c)
        return None

    # Try "B3" style
    if len(s) >= 2 and s[0].isalpha():
        col_char = s[0].upper()
        col = ord(col_char) - ord('A')
        num = s[1:]
        if num.isdigit():
            row = int(num) - 1
            if 0 <= row < size and 0 <= col < size:
                return (row, col)

    return None


def prompt_move(player: int, size: int) -> Optional[Tuple[int, int]]:
    label = "Player 1 (X, top-bottom)" if player == 1 else "Player 2 (O, left-right)"
    print(f"{label}, enter your move (e.g., '2 3' or 'B3'), or 'q' to quit: ", end="", flush=True)
    s = sys.stdin.readline().strip()
    if s.lower() in ("q", "quit", "exit"):
        return None
    mv = parse_coord(s, size)
    while mv is None:
        print(f"  ✗ Invalid input. Use 'row col' (1..{size}) or 'A1'. Try again: ", end="", flush=True)
        s = sys.stdin.readline().strip()
        if s.lower() in ("q", "quit", "exit"):
            return None
        mv = parse_coord(s, size)
    return mv


def main():
    # Prompt the user for the board size
    try:
        size = int(input("Enter board size (e.g., 5 for 5x5): ").strip())
    except ValueError:
        print("Invalid input, using default size 5.")
        size = 5

    board = HexBoard(size)

    print(f"\nStarting Hex! Board size {size}x{size}")
    board.display()
    print("\nLegend: X=Player1 (top↕bottom), O=Player2 (left↔right)\n")

    current = 1  # Player 1 starts
    while True:
        mv = prompt_move(current, size)
        if mv is None:
            print("Quit requested. Bye!")
            break
        r, c = mv

        if not board.is_valid_move(r, c):
            print("  ✗ That cell is not available. Try again.\n")
            continue

        board.make_move(r, c, current)

        print("\nBoard now:")
        board.display()
        #print(board.winner)
        


        # print(f"theeeeeee winner is: {board.winner}")
        # print(board.check_win(current, r, c))
        # #the current player is 
        # print(f"The current player is: {current}")
        # #the current move is 
        # print(f"AAThe current move is: {(r,c)}")

        if board.check_win(current, r, c):
            print(f"\n🏆 Player {current} wins!")
            break

        current = 2 if current == 1 else 1  # switch player


if __name__ == "__main__":
    main()
