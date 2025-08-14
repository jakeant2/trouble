class Board:
    def __init__(self):
        self.size = 32 # total board spaces
        #home positions to match state
        self.red_home_positions = list(range(4))
        self.blue_home_positions = list(range(16, 20))

    def is_valid_move(self, player, current_pos, steps):
        # check if move enters opponents home
        new_pos = (current_pos + steps) % self.size
        opponent_home = self.blue_home_positions if player =="RED" else self.red_home_positions
        return new_pos in opponent_home