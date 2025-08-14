from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self):
        self.color = color

    @abstractmethod
    def choose_move(self, game_state, roll):
        # returns piece index to move on game state
        pass

class Human(Player):
    def choose_move(self, game_state, roll):
        print(f"Available pieces: {self._get_movable_pieces(game_state, roll)}")
        return int(input("Choose piece (0-3): "))

    def _get_movable_pieces(self, game_state, roll):
        # help to list movable pieces
        movable = []
        pieces = game_state.red_pieces if self.color == "RED" else game_state.blue_pieces
        for i, pos in enumerate(pieces):
            if (pos == -1 and roll = 6) or (pos != -1 and pos < 28):
                movable.append(i)
        return movable