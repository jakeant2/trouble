import random
from player import Human
from agents import RuleBasedAI, RandomAI
from game_logic import GameLogic
from board import Board
from state import GameState
class GameController:
    def __init__(self, state, logic, players):
        self.state = state
        self.board = Board(self.state)
        self.logic = logic
        self.players = players
        self.current_index = 0

    def next_player(self):
        self.current_index = (self.current_index + 1) % len(self.players)
        return self.players[self.current_index]

    def play_turn(self, player):
        roll = self.logic.roll_dice()
        print(f"\n=== {player.color} TURN ===")
        print(f"Rolling dice...\nYou rolled: {roll}\n")

        choice = player.choose_move(self.state, roll)
        if choice is None:
            print("No valid moves this turn.")
            return False

        # FIX: Pass correct dicts for finish & home positions
        extra_turn = self.logic.execute_move(
            player.color,
            choice,
            roll,
            {"R": self.state.red_finish, "B": self.state.blue_finish},
            {"R": [-1, -1, -1, -1], "B": [-1, -1, -1, -1]}
        )
        self.board.display(self.state)
        return extra_turn

    def run(self):
        #players = ["RED", "BLUE"]
        #print("starting game")
        #self.board.display(self.state) # initial board
        current_idx = 0
        while not self.logic.is_game_over():
            current_player = self.players[current_idx]
            extra_turn = self.play_turn(current_player)
            #import board eachturn
            if not extra_turn:
                current_idx = (current_idx + 1) % len(self.players)

        winner = self.state.check_winner()
        print(f"\nGAME OVER! {winner} WINS!")

    """def board_display(self):
        from board import Board
        board_view = Board(self.state)
        board_view.display(self.state)"""
