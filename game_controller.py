import random
from player import Human
from agents import RandomAI, RuleBasedAI
from game_logic import GameLogic
from board import Board
from state import GameState

class GameController:
    def __init__(self):
        self.board = Board() #visualization & validation of path
        self.state = GameState() #track positions
        self.logic = GameLogic(self.board, self.state) # rules
        self.players = self._init_players() # may need to change

    def _init_players(self):
        # initialize players with types
        return [
            Human(color = "RED"),
            RuleBasedAI(color = "BLUE")
            # or RandomAI(color = "BLUE")
        ]

    def run(self):
        while not self.state.game_over:
            roll = random.randint(1, 6)
            current_player = self.players.pop(0)

            self._display_turn_start(current_player, roll) #internal help
            move_valid = False # create loop to force a valid move to be chosen
            while not move_valid:
                piece_idx = current_player.choose_move(self.state, roll) # human or AI decision
                move_valid = self.logic.validate_move(
                    player = current_player.color,
                    piece_idx = piece_idx,
                    steps = roll
                )

            self.logic.execute_move(current_player.color, piece_idx, roll)
            self.players.append(current_player)
            self._check_winner()

    def _display_turn_start(self, player, roll):
        # show board + roll info
        self.board.display(self.state)
        print(f"{player.color}'s turn - You Rolled: {roll}")

    def _check_winner(self):
        if all(pos in self.state.red_finish for pos in self.state.red_pieces):
            self.state.game_over = True
            print("RED wins!")
        elif all(pos in self.state.blue_finish for pos in self.state.blue_pieces):
            self.state.game_over = True
            print("BLUE wins!")
