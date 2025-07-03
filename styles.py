
import random

def get_move_by_style(board_copy, current_player, legal_moves, style):

    if style == "random":
        return pick_random_move(legal_moves)

    elif style == "center_bias":
        return pick_closest_to_center_move(board_copy.size, current_player, legal_moves)

    elif style == "defensive":
        return pick_defensive_move(board_copy, current_player, legal_moves)

    elif style == "aggressive":
        return pick_aggressive_move(board_copy, current_player, legal_moves)
    
    ##unkown style - for potential wrong style input
    else:
        return pick_random_move(legal_moves)


############################ styles functions ############################
def pick_random_move(legal_moves):
    return random.choice(legal_moves)


def pick_closest_to_center_move(size, current_player, legal_moves):
    if not legal_moves:
        return None
    
    center = (size // 2, size // 2)
    closest = legal_moves[0]
    min_dest = manhattan_distance(legal_moves[0],center)
    for move in legal_moves:
        dist = manhattan_distance(move,center)
        if dist < min_dest:
            min_dest = dist
            closest = move
    return closest


def pick_defensive_move(board_copy, current_player, legal_moves):
    opponent = 3 - current_player
    scores = {}
    for move in legal_moves:
        row, col = move
        neighbors = board_copy.board[row][col].get_neighbors()
        count = sum(1 for n in neighbors if n.get_cell_state() == opponent)
        scores[move] = count
    return max(scores, key=scores.get)


def pick_aggressive_move(board_copy, current_player, legal_moves):
    scores = {}
    for move in legal_moves:
        row, col = move
        neighbors = board_copy.board[row][col].get_neighbors()
        count = sum(1 for neighbor in neighbors if neighbor.get_cell_state() == current_player)
        scores[move] = count

    return max(scores, key=scores.get)


############################ helper functions ############################
def manhattan_distance(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])