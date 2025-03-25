import random
import argparse
import time



"""This is the code implementation for the Die"""
class Die:
    def __init__(self, sides=6):
        self.sides = sides
        random.seed(0) # This is for consistent results during testing.

    def roll(self):
        return random.randint(1, self.sides)

"""Implementation of the Player class"""
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def __str__(self):
        return f"{self.name} has a score of {self.score}"

# V.2: HumanPlayer, ComputerPlayer, and PlayerFactory implementation.

class HumanPlayer(Player):
    pass

class ComputerPlayer(Player):
    def decide(self, turn_total):
        threshold = min(25, 100 - self.score)
        return 'h' if turn_total >= threshold else 'r'

class PlayerFactory:
    @staticmethod
    def create_player(player_type, number):
        if player_type == "human":
            return HumanPlayer(f"Player {number}")
        elif player_type == "computer":
            return ComputerPlayer(f"CPU" if number == 1 else f"CPU {number}")
        else:
            raise ValueError("Invalid player type. Use 'human' or computer'.")


"""This is the implementation of the Game class and the Rules of the Game"""
# V.2 Need to update the Game Class to usetilize PlayerFactory.

class Game:
    def __init__(self, player1_type="human", player2_type="human"):
        self.die = Die()
        self.players = [PlayerFactory.create_player(player1_type, 1), PlayerFactory.create_player(player2_type, 2)]
        self.current_player_index = 0

    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % 2

    def play_turn(self):    # This is where the bulk of the code will go.
        current_player = self.players[self.current_player_index]
        turn_score = 0

        while True:
            roll = self.die.roll()
            print(f"{current_player.name} rolled a {roll}")

            if roll == 1:
                print(f"{current_player.name} has lost their points for this turn!")
                turn_score = 0
                break
            else:
                turn_score += roll
                print(f"Accumulated score this turn is: {turn_score}")
                # V.2: If current player is a ComputerPlayer, call decide() to automate roll/hold decision.
                if isinstance(current_player, ComputerPlayer):
                    decision = current_player.decide(turn_score)
                    print(f"{current_player.name} chooses to {'hold' if decision == 'h' else 'roll'}")
                else:
                        # Input validation to correct accepting all text as a roll.
                    while True:
                        decision = input(f"{current_player.name}, roll (r) or hold (h)? ").strip().lower()
                        if decision in ('r', 'h'):
                            break
                        else:
                            print("Invalid input. Please enter 'r' to roll or 'h' to hold")

                if decision == 'h':
                    current_player.add_score(turn_score)
                    print(f"{current_player.name} holds. Total Score: {current_player.score}")
                    break

        self.switch_turn()

    def is_game_over(self):     # Checks if game is over, Win condition.
        for player in self.players:
            if player.score >= 100:
                print(f"{player.name} wins with {player.score} points!")
                return True
        return False

    def play_game(self):
        print("Starting Pig, The Game!")
        while not self.is_game_over():
            self.play_turn()
        print("Game Over!")

""" V.2 The timed game proxy follows"""
class TimedGameProxy:
    def __init__(self, player1_type="human", player2_type="human"):
        self.game = Game(player1_type, player2_type)
        self.start_time = time.time()
        self.time_limit = 60  # seconds

    def play_game(self):
        print("Starting Timed Game of Pig! ⏱️ You have 60 seconds!")
        while not self.game.is_game_over():
            elapsed = time.time() - self.start_time     # Timer at each step. The assignment kinda reads like it's asking
            print(f"⏳ Elapsed time: {int(elapsed)}s")  # For us to keep the timer displayed at each step.
            if elapsed >= self.time_limit:
                print("\n⏰ Time's up!")
                self.declare_winner()
                return
            self.game.play_turn()
        print("Game Over!")

    def declare_winner(self):
        scores = [(player.name, player.score) for player in self.game.players]
        winner = max(scores, key=lambda x: x[1])
        print(f"🏆 {winner[0]} wins with {winner[1]} points (after 60 seconds)!")

# Using argparse to allow the user to set player types via --player1 and --player2 arguments
# Accepts 'human' or 'computer' for each player; defaults to 'human' for both

def main():
    parser = argparse.ArgumentParser(description="Play a game of Pig!")
    parser.add_argument('--player1', choices=['human', 'computer'], default='human',
                        help="Choose 'human' or 'computer' for player 1")
    parser.add_argument('--player2', choices=['human', 'computer'], default='human',
                        help="Choose 'human' or 'computer' for player 2")
    parser.add_argument('--timed', action='store_true',
                        help="Run the game with a 60-second time limit")
    args = parser.parse_args()

    if args.timed:
        game = TimedGameProxy(player1_type=args.player1, player2_type=args.player2)
    else:
        game = Game(player1_type=args.player1, player2_type=args.player2)

    game.play_game()

if __name__ == "__main__":
    main()
