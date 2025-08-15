import random

class GameLogic:
    def __init__(self, board, state):
        self.board = board
        self.state = state

    def roll_dice(self):
        return random.randint(1, 6)

    def execute_move(self, player_color, piece_idx, steps, finish_positions, home_positions):
        piece_id = f"{player_color[0]}{piece_idx+1}"
        current_pos = self.state.get_piece_pos(player_color, piece_idx)
        board = self.state.board
        # move from home
        if current_pos == -1:
            if steps == 6:
                start_pos = 0 if player_color == "RED" else 16
                self.state.update_piece_pos(piece_id, start_pos, self.state.board, finish_positions, home_positions)
                print(f"{player_color} moved piece {piece_idx+1} from home.")
                return True
            else:
                print(f"{player_color} cannot move piece {piece_idx+1} from home without a 6.")
                return False
        #standard move skipping opponent finish
        pos = current_pos
        opponent_home = self.state.blue_home if player_color == "RED" else self.state.red_home
        for _ in range(steps):
            pos = (pos + 1) % self.board.size
            #skip opponent finish
            if pos in (self.state.blue_finish if player_color == "RED" else self.state.red_finish) or pos in opponent_home:
                pos = (pos + 1) % self.board.size

        #moving to finish
        #finish_zone = finish_positions[player_color[0]]
        if pos in (finish_positions[player_color[0]]):
            occupying_piece = board[pos]
            if occupying_piece and occupying_piece.startswith(player_color[0]):  # BLOCK ONLY SAME COLOR
                print(f"{player_color} cannot move piece {piece_idx+1} to finish; slot already occupied by {occupying_piece}")
                return False
        # handling capture
        target_val = board[pos]
        if target_val and target_val.startswith("R" if player_color == "BLUE" else "B"):
            print(f"{player_color} captured {target_val}!")
            self.state.send_piece_home(target_val, board, home_positions)
            #else:
                # ValueError(f"Invalid move: landing on own piece at {pos}")
        # update position
        self.state.update_piece_pos(piece_id, pos, board, finish_positions, home_positions)
        print(f"{player_color} moved piece {piece_idx+1} to {pos}")

        return steps == 6

    """def _move_from_home(self, player, piece_idx):
        # move piece from starting position
        # determine which home positions to use based on the color
        #home_pos = self.board.red_home_positions if player == "RED" else self.board.blue_home_positions
        #get specific start position for each piece
        start_pos = 0 if player == "RED" else 16
        self.state.update_piece_pos(player, piece_idx, start_pos)
        #self.state.board[start_pos] = f"{player[0]}{piece_idx+1}"  # EDIT: set board
        print(f"{player} moved piece {piece_idx+1} from home.")
        # start position empty

    def move_piece(self, player, piece_idx, steps):
        pieces = self.state.red_pieces if player == "RED" else self.state.blue_pieces
        finish = self.state.red_finish if player == "RED" else self.state.blue_finish

        current_pos = pieces[piece_idx]
        if current_pos == -1:
            if steps == 6:
                start_pos = 0 if player == "RED" else 16
                pieces[piece_idx] = start_pos
                self.state.board[start_pos] = f"{player[0]}{piece_idx+1}"
                return True
            return False
        #dont overwrite in finish
        new_pos = (current_pos + steps) % self.board.size
        if new_pos in finish:
            pieces[piece_idx] = new_pos
            if not self.state.board[new_pos]:
                self.state.board[new_pos] = f"{player[0]}{piece_idx+1}"
            return True

        pieces[piece_idx] = new_pos
        self.state.board[new_pos] = f"{player[0]}{piece_idx+1}"
        self.state.board[current_pos] = None
        return True

    def _handle_captures(self, player, new_pos):
        # send opponent home if you land on their piece
        #identify color
        opponent = "BLUE" if player == "RED" else "RED"
        # dont capture if in finish zone
        if new_pos in self.state.red_finish or new_pos in self.state.blue_finish:
            return

        cell = self.state.board[new_pos]
        #checks if starting r or b
        if cell and cell.startswith(opponent[0]):
            # extracting # from piece
            opponent_piece = int(cell[1]) - 1
            self.state.send_piece_home(opponent, opponent_piece)"""

    def is_game_over(self):
        return self.state.check_winner() is not None
        #return winner is not None
