from colorama import Fore, Back, Style

class Board:
    def __init__(self, state):
        self.state = state
        #self.size = len(self.state.board)
        self.size = 32 # total board spaces
        #home positions to match state
        self.red_home_positions = list(range(4))
        self.blue_home_positions = list(range(16, 20))

    """def is_valid_move(self, player, current_pos, steps):
        # check if move enters opponents home
        new_pos = (current_pos + steps) % self.size
        opponent_home = self.state.blue_home if player =="RED" else self.state.red_home
        return new_pos not in opponent_home"""

    def display(self, state):
        # ascii visualization
        #state = self.state
        print("\n" + "=" * 50)
        print(f"{Fore.RED}RED HOME{Style.RESET_ALL}  : " +
                " ".join(f"R{i+1}" if pos == -1 else "  "
                         for i, pos in enumerate(state.red_pieces)))
        print(f"{Fore.BLUE}BLUE HOME{Style.RESET_ALL} : " +
              " ".join(f"B{i+1}" if pos == -1 else "  "
                       for i, pos in enumerate(state.blue_pieces)))

        print(f"\n{Fore.YELLOW}NOTE:{Style.RESET_ALL} RED finishes at 28-31(RF), BLUE finishes at 12-15(BF)")
        print(f"\n{Back.WHITE}{Fore.BLACK} MAIN TRACK {Style.RESET_ALL}")

        for i in range(0, self.size, 8):
            row = []
            for j in range(8):
                pos = i + j
                cell = state.board[pos]
                if cell:
                    color = Fore.RED if cell.startswith("R") else Fore.BLUE
                    row.append(f"{color}{cell}{Style.RESET_ALL}")
                elif pos in state.red_finish:
                    row.append(f"{Fore.RED}RF{Style.RESET_ALL}") # red finish
                elif pos in state.blue_finish:
                    row.append(f"{Fore.BLUE}BF{Style.RESET_ALL}") # blue finish
                else:
                    row.append(f"{pos:02d}")

            print(" ".join(row))
        print("=" * 50 + "\n")
