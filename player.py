from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def choose_move(self, game_state, roll):
        # returns piece index to move on game state
        pass

    def get_movable_pieces(self, game_state, roll):
        pieces = game_state.red_pieces if self.color == "RED" else game_state.blue_pieces
        finish_zone = game_state.red_finish if self.color == "RED" else game_state.blue_finish
        movable = []
        for i, pos in enumerate(pieces):
            if pos == -1 and roll == 6:  # can leave home
                movable.append(i)
            elif pos != -1 and pos not in finish_zone:  # can move on main track or wrap to finish
                distance_to_finish = (finish_zone[0] - pos) % 32
                if roll <= distance_to_finish + len(finish_zone) - 1:
                    movable.append(i)
        return movable

class Human(Player):
    def choose_move(self, game_state, roll):
        movable = self.get_movable_pieces(game_state, roll)

        if not movable:
            print(f"\nNo movable pieces! You need a 6 to leave home." if roll != 6
                  else "All pieces are already out!")
            input("Press enter to end turn")
            return None

        print(f"\nAvailable pieces: {[f'{self.color[0]}{i+1}' for i in movable]}")
        while True:
            try:
                choice = int(input("Choose a piece (1-4): ")) - 1
                if choice in movable:
                    return choice
                print(f"Invalid! Choose from: {[f'{self.color[0]}{i+1}' for i in movable]}")
            except ValueError:
                print("Please enter a # 1-4")
        #return int(input("Choose piece (0-3): "))

    """def _get_movable_pieces(self, game_state, roll):
        # help to list movable pieces
        movable = []
        pieces = game_state.red_pieces if self.color == "RED" else game_state.blue_pieces
        finish_zone = game_state.red_finish if self.color == "RED" else game_state.blue_finish
        #return [i for i, pos in enumerate(pieces)
                #if (pos == -1 and roll == 6) or (pos != -1 and pos < 28)]
        for i, pos in enumerate(pieces):
            if (pos == -1 and roll == 6):
                movable.append(i)
            elif pos != -1 and pos not in finish_zone:
                distance_to_finish = (finish_zone[0] - pos) % 32
                if roll <= distance_to_finish + len(finish_zone) - 1:
                    movable.append(i)
        return movable"""
