class GameState:
    def __init__(self):
        # -1 is home, 0-31 are board, 32+ are finished
        self.red_pieces = [-1, -1, -1, -1]
        self.blue_pieces = [-1, -1, -1, -1]

        # none = empty, as of now clear board
        self.board = [None] * 32
        #finish zones
        self.red_finish = list(range(28, 32))
        self.blue_finish = list(range(12, 16))
        #home positions
        self.red_home = list(range(4))
        self.blue_home = list(range(16, 20))

    def get_piece_pos(self, player, piece_idx):
        return self.red_pieces[piece_idx] if player == "RED" else self.blue_pieces[piece_idx]

    def update_piece_pos(self, player, piece_idx, pos):
        if player == "RED":
            self.red_pieces[piece_idx] = pos
        else:
            self.blue_pieces[piece_idx] = pos

    def send_piece_home(self, player, piece_idx):
        old_pos = self.get_piece_pos(player, piece_idx)
        if old_pos != -1 and old_pos is not None:
            self.board[old_pos] = None
        self.update_piece_pos(player, piece_idx, -1)



