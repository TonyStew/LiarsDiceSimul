from allClasses import Game
from allClasses import ComputerPlayer


def main():
    count = 10 #change this to alter the number of games that are simulated
    for i in range(count):
        game = Game()
        game.fill_players()
        game.fill_players_hands()
        game.play_game(game, f"game{i}")


if __name__ == '__main__':
    main()
