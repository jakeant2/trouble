class GameState:
    def __init__(self):
        # -1 is home, 0-31 are board, 32+ are finished
        self.red_pieces = [-1, -1, -1, -1]
        self.blue_pieces = [-1, -1, -1, -1]
        # none = empty, as of now clear board
        self.board = [None for _ in range(32)]
        #finish zones
        self.red_finish = [28, 29, 30, 31]
        self.blue_finish = [12, 13, 14, 15]
        #home positions
        self.red_home = [-1, -1, -1, -1]#list(range(4))
        self.blue_home = [-1, -1, -1, -1]#list(range(16, 20))

        #self.game_over = False

    def get_piece_pos(self, player, piece_idx):
        #if piece_idx is None or not isinstance(piece_idx, int) or not (0 <= piece_idx < 4):
            #return -2
        return self.red_pieces[piece_idx] if player == "RED" else self.blue_pieces[piece_idx]

    def update_piece_pos(self, piece_id, new_pos, board, finish_positions, home_positions):
        # remove from current position
        for i, val in enumerate(board):
            if val == piece_id:
                board[i] = None  # restore default square label
                break

        color = piece_id[0]  # "R" or "B"
        # 2 -check if moving into finish zone
        if new_pos in finish_positions[color]:
            if board[new_pos] is not None:
                raise ValueError(f"Invalid move: {piece_id} tried to enter finish slot already occupied by {board[new_pos]}")
            board[new_pos] = piece_id
            if color == "R":
                self.red_pieces[int(piece_id[1]) - 1] = new_pos
            else:
                self.blue_pieces[int(piece_id[1])- 1] = new_pos
            return

        board[new_pos] = piece_id
        if color == "R":
            self.red_pieces[int(piece_id[1]) - 1] = new_pos
        else:
            self.blue_pieces[int(piece_id[1])- 1] = new_pos

    def send_piece_home(self, piece_id, board, home_positions):
        color = piece_id[0]
        idx = int(piece_id[1]) - 1
        if color == "R":  # empty home slot
            self.red_pieces[idx] = -1
        else:
            self.blue_pieces[idx] = -1
        home_slots = home_positions[color]
        for pos in home_slots:
            if board[pos] is None:
                board[pos] = piece_id
                return
        #raise RuntimeError(f"No home slot available for {piece_id}")


    def check_winner(self):
        # update game-over status & return winner
        if all(pos in self.red_finish for pos in self.red_pieces):
                self.game_over = True
                return "RED"
        if all(pos in self.blue_finish for pos in self.blue_pieces):
                self.game_over = True
                return "BLUE"
        return None

    def is_vulnerable(self, player, position):
        #check if could be captured by opponent
        if not (0 <= position < len(self.board)):
            return False

        #opponent = "BLUE" if player == "RED" else "RED"
        opponent_positions = self.blue_pieces if player == "RED" else self.red_pieces
        #can an opponent roll the right # to reach your position?
        for opp_pos in opponent_positions:
            if 0 <= opp_pos < len(self.board):
                distance = (position - opp_pos) % len(self.board)
                if 1 <= distance <= 6:
                    return True
        return False
