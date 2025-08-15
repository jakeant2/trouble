#start the game
from game_controller import GameController
from state import GameState
from game_logic import GameLogic
from player import Human
from agents import RuleBasedAI, RandomAI
from board import Board


if __name__ == '__main__':
    state = GameState()
    board = Board(state)
    logic = GameLogic(board,state)
    red_player = Human("RED")
    blue_player = RuleBasedAI("BLUE")
    players = [red_player, blue_player]

    game = GameController(state, logic, players)
    game.run()
