from simulation import simulate_game_from_move

class Agent:

    def __init__(self, player, style = "random", num_simulations = 100):

        "initializes the agent"
        self.player = player
        self.style = style
        self.num_simulations = num_simulations
    

    def choose_move(self,board):
        # For each legal move:
        #   - run evaluate_move()
        #   - pick the move with highest win rate
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None
        
        best_move = legal_moves[0]
        max_eval = -1
        for move in legal_moves:
            eval = self.evaluate_move(board,move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
                
        return best_move
    
    def evaluate_move(self,board, move):
        # Run num_simulations playouts starting with move
        # Return fraction of wins by player
        wins = 0
        for i in range(self.num_simulations):
            winner = self.simulate_game(board,self.style, self.player,move) #add rest of params!
            if winner == self.player:
                wins+=1
        
        return wins/self.num_simulations


    def simulate_game(self,board,style,player, move):
        # Run one playout from board, biased by style
        # Return winner
        return simulate_game_from_move(board,player,style,move)
