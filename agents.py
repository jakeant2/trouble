import random
from player import Player

class RandomAI(Player):
    # move random piece
    def choose_move(self, game_state, roll):
        pieces = game_state.red_pieces if self.color == "RED" else game_state.blue_pieces
        movable = [i for i, pos in enumerate(pieces)
                   if (pos == -1 and roll == 6) or (pos != -1 and pos < 28)]
        return random.choice(movable) if movable else None

class RuleBasedAI(Player):
    #prioritize sending pieces home, attacking other players pieces
    # define scores for each
    FINISH_SCORE = 100
    CAPTURE_SCORE = 50
    SAFE_SPACE_SCORE = 10
    def choose_move(self, game_state, roll):
        # select optimal move based on rules
        movable_pieces = self.get_movable_pieces(game_state, roll)
        if not movable_pieces:
            return None

        #rank by priority
        best_move, best_score = None, -1

        for piece_idx in movable_pieces:
            score = self._evaluate_move(game_state, piece_idx, roll)
            # looping through all possible moves - maybe not the fastest way to do it but i am not the best coder ever and this project is far too complicated for me so here we go
            if score > best_score:
                best_score = score
                best_move = piece_idx
                if best_score == self.FINISH_SCORE:
                    break
        return best_move

    def _evaluate_move(self, game_state, piece_idx, roll):
        #score a move - higher is better
        current_pos = game_state.get_piece_pos(self.color, piece_idx)
        new_pos = (current_pos + roll) % 32
        score = 0

        # first priority - finishing a piece
        if self.color =="RED" and new_pos in game_state.red_finish:
            if (current_pos + roll) == (28 + piece_idx):
                return self.FINISH_SCORE
        elif self.color =="BLUE" and new_pos in game_state.blue_finish:
            if (current_pos + roll - 16) % 32 == (12 + piece_idx):
                return self.FINISH_SCORE

        # priority 2 - sending an opponent home
        opponent = "BLUE" if self.color == "RED" else "RED"
        if game_state.board[new_pos] and game_state.board[new_pos].startswith(opponent[0]):
            score += self.CAPTURE_SCORE # high reward, not as high as 100

        #priority 3 - moving towards home
        score += new_pos if self.color == "RED" else (new_pos - 16) % 32

        # Safer space bonus only if not vulnerable
        if not game_state.is_vulnerable(self.color, new_pos):
            score += self.SAFE_SPACE_SCORE

        return score

    """def _get_movable_pieces(self, game_state, roll):
        #return positions of pieces that can move this turn
        pieces = game_state.red_pieces if self.color == "RED" else game_state.blue_pieces
        #movable = []
        return [i for i, pos in enumerate(pieces)
            if (pos == -1 and roll == 6) or (0 <= pos < 28)]
"""
