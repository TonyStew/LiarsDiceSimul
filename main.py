from allClasses import Game

from allClasses import UserPlayer
from allClasses import ComputerPlayer


def main():
    count = 10
    for i in range(count):
        # we have a single game
        game = Game()
        # game is set up
        game.fill_players()
        game.fill_players_hands()
        # for sure works until this point

        # complete toss up
        game.play_game(game, f"game{i}")


if __name__ == '__main__':
    main()
