import random
from collections import Counter

class Dice:

    def __init__(self):
        self.rolled_number = 0

    def roll_one_dice(self):
        self.rolled_number = random.randint(1, 6) #this is where you would change the possible dice faces

data = []

class Player:

    def __init__(self):
        self.quantity_wager = 0
        self.die_wager = 0
        self.player_hand = []

        # number of die in players hand this is for computer purposes
        self.number_of_die_inHand = 0
        # required minimum quantity wager this is for computer purposes
        self.minimum_quantity_wager = 0
        # percent of the unsure dice that must be applicable to wager this is for computer purposes
        self.percent_of_unsure_must_be_applicable = 0.000


    def print_wager(self):
        print(f'{self.name} quantity wager: {self.quantity_wager}')
        print(f'{self.name} die wager: {self.die_wager}')

    #init the player's hand of dice
    def fill_hand(self):
        while len(self.player_hand) < 4: #this is where you would change the number of dice per player
            dice = Dice()
            self.player_hand.append(dice)

    #roll all the player's dice
    def roll_hand(self):
        for dice in self.player_hand:
            dice.roll_one_dice()

    #used when a player decides to call liar
    def call_liar(self, game):
        dice_on_table_list = []
        print(f'{self.name} called liar')
        #count up the dice
        for player in game.players:
            for dice in player.player_hand:
                if dice.rolled_number == game.die_wager:
                    game.die_wager_counter += 1
                dice_on_table_list.append(dice.rolled_number)

        for player in game.active_players:
            for dice in player.player_hand:
                if dice.rolled_number == game.die_wager:
                    game.die_wager_counter += 1
                dice_on_table_list.append(dice.rolled_number)

        print('The dice on the table are:')
        print(*dice_on_table_list)
        #figure out who was right and have them lose a dice
        if game.quantity_wager > game.die_wager_counter:
            liar = game.active_players[0]
            liar.player_hand.pop(0)
            print(f'{liar.name} loses a dice')
        elif game.quantity_wager <= game.die_wager_counter:
            wageree = game.active_players[1]
            wageree.player_hand.pop(0)
            print(f'{wageree.name} loses a dice')

        game.reset_players_lists()
        game.clear_wagers()
        print('')

    #reset this players wagers
    def clear_player_wagers(self):
        self.die_wager = 0
        self.quantity_wager = 0

class ComputerPlayer(Player):

    def __init__(self, name):

        # computer name
        self.name = name

        # creates a list of die lists, each die has a number of die, a weighted value, and the number
        #this code is for the probabilistic model
        self.die1 = [0, 0, 1]
        self.die2 = [0, 0, 2]
        self.die3 = [0, 0, 3]
        self.die4 = [0, 0, 4]
        self.die5 = [0, 0, 5]
        self.die6 = [0, 0, 6]


        # list of die lists
        self.die_list = [self.die1, self.die2, self.die3, self.die4, self.die5, self.die6]

        # threshold percentage for wager
        self.threshold_percent = 0.45

        # initializes everything from the parent class Player
        super().__init__()

    #This is part of the probabilistic implementation, we won't need this with state based strategies
    def count_dice(self):
        self.number_of_die_inHand = 0
        # self.die1 = [0, 0, 1]
        # self.die2 = [0, 0, 2]
        # self.die3 = [0, 0, 3]
        # self.die4 = [0, 0, 4]
        # self.die5 = [0, 0, 5]
        # self.die6 = [0, 0, 6]
        # counts the number of each dice in the hand
        # put in decimals to add value to a 6 (ie. wager on a six before a 1)
        for dice in self.player_hand:

            self.number_of_die_inHand += 1
            if dice.rolled_number == 1:
                self.die1[0] += 1
                self.die1[1] += 1.01
            elif dice.rolled_number == 2:
                self.die2[0] += 1
                self.die2[1] += 1.02
            elif dice.rolled_number == 3:
                self.die3[0] += 1
                self.die3[1] += 1.03
            elif dice.rolled_number == 4:
                self.die4[0] += 1
                self.die4[1] += 1.04
            elif dice.rolled_number == 5:
                self.die5[0] += 1
                self.die5[1] += 1.05
            elif dice.rolled_number == 6:
                self.die6[0] += 1
                self.die6[1] += 1.06

    def find_max(self):
        die_counter_list = []
        for die in self.die_list:
            die_counter_list.append(die[1])
        max_counter = max(die_counter_list)
        for die in self.die_list:
            if die[1] == max_counter:
                return die

    def calculate_the_minimum_wager_quantity(self, game):
        max_die = self.find_max()
        if game.die_wager == 0 and game.quantity_wager == 0:
            self.minimum_quantity_wager = game.quantity_wager + 1
        elif max_die[2] > game.die_wager:
            self.minimum_quantity_wager = game.quantity_wager
        elif max_die[2] <= game.die_wager:
            self.minimum_quantity_wager = game.quantity_wager + 1

    #this is the main component of the probabilistic model, it is currently not being called
    #I only left it as a reference
    def calculate_odds_of_required_wager(self, game):
        # The die object that the computer has the most of
        max_die = self.find_max()
        # The total amount of dice on the table
        total_dice = game.total_dice_on_table
        # The number of dice that it posses applicable to the wager
        number_of_applicable_dice = max_die[0]
        # the number of dice it has in its hand
        number_of_possessed_dice = self.number_of_die_inHand
        # required quantity wager for wager
        minimum_quantity_wager = self.minimum_quantity_wager
        # Number of dice the computer is unsure about on the table
        unsure_dice = total_dice - number_of_possessed_dice
        # The min quanity - applicable dice
        cover_amount = minimum_quantity_wager - number_of_applicable_dice
        # percent of dice on the table required to be of applicable
        percent_of_unsure_must_be_applicable = cover_amount/unsure_dice
        self.percent_of_unsure_must_be_applicable = percent_of_unsure_must_be_applicable

    def clear_die_counters(self):
        for die in self.die_list:
            die[0] = 0
            die[1] = 0

    #this and the next two functions are what determines how the AI players act, if you want to change how they wager, alter this function
    def wager(self, game, dice_vals, most_common):
        if most_common[1] > game.quantity_wager or (most_common[1] == game.quantity_wager and most_common[0] > game.die_wager):
            game.quantity_wager = most_common[1]
            game.die_wager = most_common[0]
        elif most_common[1] >= 2 and most_common[0] != game.die_wager and game.quantity_wager <= 3 * most_common[1]:
            if most_common[0] <= game.die_wager:
                game.quantity_wager += 1
            game.die_wager = most_common[0]
        elif dice_vals.count(game.die_wager) >= 1 and game.quantity_wager <= 3 * dice_vals.count(game.die_wager):
            game.quantity_wager += 1
        self.quantity_wager = game.quantity_wager
        self.die_wager = game.die_wager
        self.print_wager()
        game.add_next_active_player()

    #this function is where the computer players determine if they want to call liar or if they want to wager
    def decide(self, game):
        dice_vals = [i.rolled_number for i in self.player_hand]
        most_common = Counter(dice_vals).most_common(1)[0]
        if (most_common[1] > game.quantity_wager or (most_common[1] == game.quantity_wager and most_common[0] > game.die_wager))\
                or (most_common[1] >= 2 and most_common[0] != game.die_wager and game.quantity_wager <= 3 * most_common[1])\
                or (dice_vals.count(game.die_wager) >= 1 and game.quantity_wager <= 3 * dice_vals.count(game.die_wager)):
            self.wager(game, dice_vals, most_common)
        else:
            self.call_liar(game)

    #this function is called when the game wants this agent to make a move (when it's their turn)
    def wager_or_liar(self, game):
        self.decide(game)

class Game:

    def __init__(self):
        self.total_dice_on_table = 0
        self.quantity_wager = 0
        self.die_wager = 0
        self.die_wager_counter = 0
        self.players = []
        self.active_players = []

    def fill_players(self):
        player_names_list = ['Hal', 'Allice', 'WOPR', 'Andy']
        # while len(self.players) < 1:  #loop for generating the human players
        #     username = input('What is your name?')
        #     player = UserPlayer(username)
        #     self.players.append(player)
        while len(self.players) < 4: #loop for generating AI players
            for player_name in player_names_list:
                player = ComputerPlayer(player_name)
                self.players.append(player)

    def fill_players_hands(self):
        for player in self.players:
            player.fill_hand()

    #done every round
    def all_players_roll(self):
        # all players roll dice
        for player in self.players:
            player.roll_hand()

    #sum all the remaining dice
    def calculate_dice_left(self):
        self.total_dice_on_table += sum(len(player.player_hand) for player in self.players)
        self.total_dice_on_table += sum(len(player.player_hand) for player in self.active_players)
        print(f'{self.total_dice_on_table} dice are on the table')

    def check_players_elgibility(self): #remove losers from the game
        for player in self.players:
            if len(player.player_hand) == 0: #if any player is out of dice
                print(f'{player.name} is out of dice')
                self.players.remove(player) #remove them from the player list

    def choose_active_players(self): #pick the next player as active
        while len(self.active_players) < 2: #while there is only one active player
            popped_player = self.players.pop(0) #pop a player off the list
            self.active_players.append(popped_player) #add them as the active player

    #add the next player as active
    def add_next_active_player(self):
        if len(self.players) > 0:
            while len(self.active_players) < 3:
                popped_player = self.players.pop(0)
                self.active_players.append(popped_player)
        elif len(self.players) <= 0:
            popped_player = self.active_players.pop(0)
            self.active_players.append(popped_player)

    #remove the oldest active player
    def remove_old_active_player(self):
        while len(self.active_players) > 2:
            popped_player = self.active_players.pop(0)
            self.players.append(popped_player)

    #take all the players out of active and put them back into the normal list
    def reset_players_lists(self):
        while len(self.active_players) > 0:
            popped_player = self.active_players.pop(0)
            self.players.append(popped_player)

    #have the active player start the wagering
    def set_first_wager(self, game):
        if self.die_wager == 0 and self.quantity_wager == 0:
            player = self.active_players[0]
            player.decide(game)
            if len(self.players) == 0:
                self.add_next_active_player()

    #have all the players wager until one calls liar
    def play_out_round(self, game):
        while self.die_wager != 0 or self.quantity_wager != 0:
            #update the current and previous players
            active_player = self.active_players[1]
            previous_active_player = self.active_players[0]
            #tell the active player to wager or call liar
            active_player.wager_or_liar(game)
            if len(self.active_players) > 0:
                #add the wager values to the list of data
                data.append([active_player.name, active_player.die_wager, active_player.quantity_wager, {i.name:[j.rolled_number for j in i.player_hand] for i in (self.active_players + self.players)}])
            else:
                #add the Liar row to the list of data
                data.append([active_player.name, "LIAR", "LIAR", {i.name:[j.rolled_number for j in i.player_hand] for i in (self.active_players + self.players)}])
            #if a player's wager is beat, remove them from the active players
            if previous_active_player.quantity_wager < active_player.quantity_wager and len(self.players) > 0:
                self.remove_old_active_player()
            elif previous_active_player.quantity_wager == active_player.quantity_wager and len(self.players) > 0:
                if previous_active_player.die_wager < active_player.die_wager:
                    self.remove_old_active_player()

    def play_round(self, game):
        self.check_players_elgibility() #check and remove players with no dice
        self.all_players_roll() #roll all the players dice
        self.choose_active_players() #assign the active player to be the next player in the queue
        self.calculate_dice_left() #update the number of remaining dice
        self.set_first_wager(game) #have the starting player initiate the betting
        self.play_out_round(game) #have all the players wager until one calls liar
        self.check_players_elgibility() #again, check and remove players have lost
        self.clear_variables_in_players() #reset all players' variables (wagers and dice)

    #reset a player for a new round
    def clear_wagers(self):
        self.quantity_wager = 0
        self.die_wager = 0
        self.total_dice_on_table = 0
        self.die_wager_counter = 0

    #reset all players for a new round
    def clear_variables_in_players(self):
        for player in self.players:
            player.number_of_die_inHand = 0
            player.minimum_quantity_wager = 0
            player.percent_of_unsure_must_be_applicable = 0

    #this function runs the simulation
    def play_game(self, game, game_name):
        while len(self.players) > 1: #while there is more than one player in the game
            self.play_round(game) #play a round
            # for player in self.players: #this is used for the probabilistic model
            #     player.clear_die_counter()
        for player in self.players: #find the remaining player
            print(f'{player.name} won the game!') #announce their victory
        import pandas as pd
        df = pd.DataFrame(data, columns = ['name', 'wager', 'wager_count', 'player_hands']) #create a df from the list of rounds
        df.to_csv(game_name + '.csv', encoding='utf-8', index=False) #save the df as a csv
