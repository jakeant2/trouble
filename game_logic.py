import random

class GameController:
    def __init__(self, players=2):
        self.players = players
        self.board = {player: [0, 0, 0, 0] for player in range(players)}  # Each player has 4 tokens at start
        self.home = {player: 0 for player in range(players)}  # Track tokens that reached "home"

    def roll_dice(self):
        return random.randint(1, 6)

    def move_token(self, player, token_index, roll):
        if self.board[player][token_index] == 0 and roll == 6:  # Token can only leave start with a 6
            self.board[player][token_index] = 1
        elif self.board[player][token_index] > 0:  # Move token forward
            self.board[player][token_index] += roll
            if self.board[player][token_index] > 28:  # Assuming 28 spaces to "home"
                self.board[player][token_index] = 28
                self.home[player] += 1

    def check_collision(self, player, token_index):
        position = self.board[player][token_index]
        for opponent in self.board:
            if opponent != player:
                for i, pos in enumerate(self.board[opponent]):
                    if pos == position and position != 0:  # Collision detected
                        self.board[opponent][i] = 0  # Send opponent's token back to start


    def play_turn(self, player):
        roll = self.roll_dice()
        for i, token in enumerate(self.board[player]):
            if token < 28:  # Only move tokens not already home
                self.move_token(player, i, roll)
                self.check_collision(player, i)
                break  # Move one token per turn
        if roll == 6:  # Roll again if a 6 is rolled
            self.play_turn(player)

    def is_winner(self, player):
        return self.home[player] == 4  # All 4 tokens must be home to win, change this if we don't use all 4

    def play_game(self):
        turn = 0
        while True:
            current_player = turn % self.players
            self.play_turn(current_player)
            if self.is_winner(current_player):
                break
            turn += 1
