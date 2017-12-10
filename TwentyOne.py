# Dealer could be an object... hits on soft_16, soft_17
# Game could be an object
# Display graphics could be an action
# Need to use try statements to capture bad inputs like char for int
# Implement split option  -- requires hands to become a dict
# Add up to three players
# Make an AI to play as the player
# Allow prop bets and insurance
# payout 1.5 times for blackjack

import random
import sys


class Deck(object):
    def __init__(self, number_of_decks):
        # create a new deck of cards built of one or more decks
        card_values = '23456789DJQKA'
        card_suits = '♠♦♥♣' * number_of_decks
        self.card_list = [(v, s) for s in card_suits for v in card_values]

    def draw(self, hand):
        # remove a card from the deck and return the card
        hand.cards.append(self.card_list.pop(0))
        hand.calculate_score()

    def shuffle(self):
        # change position of all cards in the card list
        random.shuffle(self.card_list)


class Hand(object):
    def __init__(self, player_object):
        self.bet = 0
        self.cards = []
        self.player = player_object
        self.result = ''
        self.score = 0

    def double_bet(self):

        # double the hand's bet if they have enough dollars available
        if 0 <= int(self.bet * 2) <= self.player.dollars:
            self.player.dollars -= self.bet
            self.bet = self.bet * 2
            return True
        return False

    def place_bet(self, bet, table):
        if (0 <= bet <= self.player.dollars) and table.legal_bet(bet):
            self.bet = bet
            self.player.dollars -= bet
            return True
        return False

    def reset(self):
        # change player values to initial values at the start of a new round
        self.bet = 0
        self.cards = []

    def calculate_score(self):
        # initialize variable to track score
        hand_value = 0

        # look at each card and add value to score
        for card in self.cards:
            if card[0] in ['D', 'J', 'Q', 'K']:
                hand_value += 10
            elif card[0] == 'A':
                hand_value += 11
            else:
                hand_value += int(card[0])

        # if the hand is over 21 and has one or more aces reduce the value of aces until score is 21 or less
        if hand_value > 21 and 'A' in self.cards:
            for n in range(self.cards.count('A')):
                hand_value -= 10
                if hand_value <= 21:
                    break

        # if the hand is over 21 then the player busts and score equals 0
        if hand_value > 21:
            hand_value = 0
        self.score = hand_value


class Player(object):
    def __init__(self, name, dollars):
        self.name = name
        self.dollars = dollars


class Table(object):
    def __init__(self, min_bet, max_bet):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.soft_17 = False

    def legal_bet(self, bet):

        # check if the player's bet is within table limits
        if self.min_bet <= bet <= self.max_bet:
            return True
        else:
            return False


# game is definitely a class

# game variables
min_bet = 10
max_bet = 100
number_of_decks = 6
reset_deck = 78
player_starting_dollars = 500

# display game title and author
print('\n======================================================\n'
      '♠♦♥♣   TwentyOne - Written By: Matthew Devaney   ♠♦♥♣\n'
      '======================================================\n')

# setup table
t = Table(min_bet, max_bet)

# setup deck
d = Deck(number_of_decks)
d.shuffle()

# create empty lists to store the location of hand and player objects
hands_list = []
players_list = []

# setup dealer
p = Player('Dealer', 0)
players_list.append(p)

while True:

    # setup players and assign an empty hand
    player_name = input('Enter player name: ')
    p = Player(player_name, player_starting_dollars)
    players_list.append(p)
    action = str.lower(input('Add another player? (Y)es, (No): '))
    print()
    if action == 'y':
        pass
    elif action == 'n':
        break
    else:
        print('Invalid input.  Please choose \'Y\' or \'N\'')

while True:

    # create and empty hand for the dealer and each player
    hands_list = []
    for player in players_list:
        hands_list.append(Hand(player))

    # ask each player to make a bet
    for hand in hands_list[1:]:

        bet_successfully_placed = False

        while not bet_successfully_placed:
            try:
                player_bet = int(input('{} has {} dollars.\nHow much would you like to bet? (Min={}, Max={}) '
                                       .format(hand.player.name, hand.player.dollars, t.min_bet, t.max_bet)))
                print()
                bet_successfully_placed = hand.place_bet(int(player_bet), t)
                if not bet_successfully_placed:
                    print('Invalid bet.  Must be within table limits and player must have dollars available.\n')
            except ValueError:
                print('\nInvalid bet. Must input a number value not a string\n')
                continue

    # check how many cards are in the deck to see if a new shoe is necessary
    if len(d.card_list) <= reset_deck:
        d = Deck(number_of_decks)
        d.shuffle()

    # deal cards to each player and dealer
    for n in range(2):
        for hand in hands_list:
            d.draw(hand)

    # set the current hand to the 1st player at list position 1 skipping the dealer at position 0
    hand_position = 1

    # set the current hand indicator graphic to blank
    current_hand_indicator = ''

    while True:

        # display all hands at table while hiding the dealer's 1st card
        print('{}\'s Hand: [(\'?\',\'?\'), {}]  Score=???'
              .format(hands_list[0].player.name, hands_list[0].cards[1]))

        for n in range(1, len(hands_list)):
            if n == hand_position:
                current_hand_indicator = '> '
            else:
                current_hand_indicator = ''
            print('{}{}\'s Hand: {}  Score={}, Bet={}'
                  .format(current_hand_indicator, hands_list[n].player.name, hands_list[n].cards, hands_list[n].score,
                          hands_list[n].bet))

        if hands_list[hand_position].score == 21:
            hand_position += 1
        else:
            # ask the user what action they would like to take
            action = str.lower(input('\n{}\'s Turn : What would you like to do? (H)it, (S)tand, (D)ouble, S(p)lit? '
                                     .format(hands_list[hand_position].player.name)))
            print()

            # take action based on player response
            if action == 'h':
                d.draw(hands_list[hand_position])

                # check if player busts or has a score of 21
                if hands_list[hand_position].score == 0 or hands_list[hand_position].score == 21:
                    hand_position += 1
            elif action == 's':
                hand_position += 1
            elif action == 'd':
                if hands_list[hand_position].double_bet():
                    d.draw(hands_list[hand_position])
                    hand_position += 1
                else:
                    print('\n{} does not enough dollars to double hand\n'.format(hands_list[hand_position].player.name))
            else:
                print('\n' + 'Invalid input. Please choose \'H\', \'S\',\'D\' or \'P\'.\n')

        if hand_position >= len(hands_list) or hands_list[hand_position].score == 0:
            break

    # dealer's turn
    while True:
        if hands_list[0].score == 17 and 'A' in hands_list[0].cards and t.soft_17:
            d.draw(hands_list[0])
            t.soft_17 = True
        elif hands_list[0].score < 17:
            d.draw(hands_list[0])
        elif hands_list[0].score > 17 or \
                (hands_list[0].score == 17 and 'A' not in hands_list[0].cards):
            break
        if hands_list[0].score == 0:
            break

    for hand_position in range(1, len(hands_list)):
        # determine the result of each hand and change dollars for the player

        if hands_list[hand_position].score > hands_list[0].score and hands_list[hand_position].score == 21 \
                and (hands_list[hand_position]) == 2:
            hands_list[hand_position].player.dollars += hands_list[hand_position].bet * 1.5
            hands_list[hand_position].result = 'BLACKJACK'
        elif hands_list[hand_position].score > hands_list[0].score:
            hands_list[hand_position].player.dollars += hands_list[hand_position].bet * 2
            hands_list[hand_position].result = 'WIN'
        elif hands_list[hand_position].score < hands_list[0].score or hands_list[hand_position].score == 0:
            hands_list[hand_position].result = 'LOSE'
        elif hands_list[hand_position].score == hands_list[0].score:
            hands_list[hand_position].player.dollars += hands_list[hand_position].bet
            hands_list[hand_position].result = 'TIE'

    print('Result:')
    print('{}\'s Hand: {}  Score={}'
          .format(hands_list[0].player.name, hands_list[0].cards, hands_list[0].score))
    for n in range(1, len(hands_list)):
        print('{}\'s Hand: {}  Result={}, Score={}, Bet={}, '
              .format(hands_list[n].player.name, hands_list[n].cards, hands_list[n].result, hands_list[n].score,
                      hands_list[n].bet))
    print()

    # check if each player has enough dollars to continue playing
    player_position = 1

    while True:
        if player_position >= len(players_list):
            break
        elif players_list[player_position].dollars == 0 or players_list[player_position].dollars < t.min_bet:
            print('{} does not have enough dollars to continue. Thank you for playing TwentyOne\n'
                  .format(players_list[player_position].name))
            players_list.remove(player_position)
        player_position += 1

    # end game if no more players are remaining
    if len(players_list) == 1:
        print('No more players remaining.  Thank you for playing TwentyOne.')
        sys.exit()
