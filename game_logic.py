class GameLogic:
    def __init__(self, board, state):
        self.board = board
        self.state = state


    def validate_move(self, player, piece_idx, steps):
        # check if move is legal - t/f
        current_pos = self.state.get_piece_pos(player, piece_idx)
        #rule 1 - starting from home requires a 6
        if current_pos == -1:
            return steps == 6 # can only leave if 6

        # rule 2 - cannot enter opponents home
        if not self.board.is_valid_move(player, current_pos, steps):
            return False

        # rule 3 must land exactly in finish
        new_pos = (current_pos + steps) % self.board.size
        if player == "RED" and new_pos in self.state.red_finish:
            return (current_pos + steps) == (28 + piece_idx)
        elif player == "BLUE" and new_pos in self.state.blue_finish:
            return (current_pos + steps - 16) % 32 == (12 + piece_idx)

        return True


    def execute_move(self, player, piece_idx, steps):
        # process the move
        if not self.validate_move(player, piece_idx, steps):
            raise ValueError("Illegal move attempted - invalid finish or blocked home")

        current_pos = self.state.get_piece_pos(player, piece_idx)
        #starting form home
        if current_pos == -1:
            self._move_from_home(player, piece_idx)
            return

        #standard movement
        new_pos = (current_pos + steps) % self.board.size

        #to handle trouble - landing on opponent
        if (player == "RED" and new_pos not in self.state.red_finish) or \
        (player == "BLUE" and new_pos not in self.state.blue_finish):
            self._handle_captures(player, new_pos)

        #update position
        self.state.update_piece_pos(player, piece_idx, new_pos)

    def _move_from_home(self, player, piece_idx):
        # move piece from starting position
        # determine which home positions to use based on the color
        home_pos = self.board.red_home_postions if player == "RED" else self.board.blue_home_postions
        #get specific start position for each piece
        start_pos = home_pos[piece_idx]
        # start position empty
        if self.state.board[start_pos] is None:
            self.state.board[start_pos] = f"{player[0]}{piece_idx+1}"
            self.state.set_piece_pos(player, piece_idx, start_pos)

    def _handle_captures(self, player, new_pos):
        # send opponent home if you land on their piece
        #identify color
        opponent = "BLUE" if player == "RED" else "RED"
        #check if new position has an opponent's piece
        if self.state.board[new_pos] and self.state.board[new_pos].startswith(opponent[0]):
            #extract opponents piece index
            opponent_piece = int(self.state.board[new_pos][1]) - 1
            self.state.send_piece_home(opponent, opponent_piece)

