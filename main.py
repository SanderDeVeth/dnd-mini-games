import random
import os
from enum import Enum

class textDecorations:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

DEALER_STANDS = 17
TARGET_SCORE = 21
STARTING_HAND_LENGTH = 2

def clear():
    _ = os.system('cls' if os.name == 'nt' else 'clear')

# TODO: Player class 
# TODO: Player class has state (money, bet, hand, score)
# TODO: Player class has methods (hit, stand, double, split)
# TODO: Player class has properties (is_busted, is_blackjack)
# TODO: Player can bet
# TODO: Player can split
# TODO: Dealer class (inherits from Player class)
# TODO: Deck class (manages deck of cards)
# TODO: Game class (manages game state, players, deck, etc.
# TODO: Pretty print cards
# TODO: Add more players
# TODO: Add variant rules (dealer checks for blackjack on 10 or A face up card (reveal if true), dealer hits on soft 17, dealer receives one card at start, etc.)

class turnStates(Enum):
    BETTING = 0
    DEALING = 1
    PLAYING = 2
    DEALER = 3
    END = 4

# BLACKJACK is max score of 21 with two cards
# WIN is when player has higher score than dealer
# LOSE is when player has less score than dealer
# PUSH is when player and dealer have the same score
# BUST is when player has more than the max score of 21
class WinStates(Enum):
    BLACKJACK = 1
    WIN = 2
    LOSE = 3
    PUSH = 4
    BUST = 5

class Card:
    def __init__(self, suit, rank, value):
        # Suit of the Card like Spades and Clubs
        self.suit = suit    

        # Representing Rank of the Card like A for Ace, K for King
        self.rank = rank
        
        # Score Value for the Card like 10 for King
        self.value = value

def blackjack_game(deck):
    global rank_values
    
    # cards
    player_hand = []
    dealer_hand = []
    
    # scores
    player_score = 0
    dealer_score = 0

    clear()

# Phase 0: Deal 2 cards to everyone (players first, dealer last)
    while len(player_hand) < STARTING_HAND_LENGTH:
        # deal random card to player
        player_card = deal_card(deck, player_hand)
        player_score += player_card.value

        # Check for double Ace
        if(len(player_hand) == STARTING_HAND_LENGTH):
            if player_hand[0].value == "11" and player_hand[1].value == "A":
                player_hand[0].value = "1"
                player_score -= 10

    while len(dealer_hand) < STARTING_HAND_LENGTH:
        # deal random card to dealer
        dealer_card = deal_card(deck, dealer_hand)

        # update dealer's score
        dealer_score += dealer_card.value

    # Check for double Ace
    if(len(dealer_hand) == STARTING_HAND_LENGTH):
        if dealer_hand[0].value == "11" and dealer_hand[1].value == "A":
            dealer_hand[1].value = "1"
            dealer_score -= 10

# Phase 1: Player's Turn
    player_turn(player_hand, dealer_hand)
    
# Phase 2: TODO: Place bets
    
# Phase 3: Dealer's Turn
    # managing dealer's turn
    # dealer's score is less than 17
    dealer_turn(player_hand, dealer_hand)
    round_end(player_hand, dealer_hand, dealer_hidden=True)

##########################################################################################################
#                                            HELPER FUNCTIONS                                            #
##########################################################################################################

def calc_score(hand):
    score = 0
    for card in hand:
        score += card.value
    return score

def deal_card(deck, hand):
    card = random.choice(deck)
    hand.append(card)
    deck.remove(card)
    return card

def win_state(player_hand, dealer_hand):
    player_score = calc_score(player_hand)
    dealer_score = calc_score(dealer_hand)
    
    if player_score > TARGET_SCORE:
        return WinStates.BUST
    if player_score == dealer_score:
        return WinStates.PUSH
    if player_score < dealer_score and dealer_score <= TARGET_SCORE:
        return WinStates.LOSE
    if player_score == TARGET_SCORE and len(player_hand) == 2 and dealer_score != TARGET_SCORE:
        return WinStates.BLACKJACK
    if player_score > dealer_score or dealer_score > TARGET_SCORE:
        return WinStates.WIN

def win_message(turn_state):
    match turn_state:
        case WinStates.BLACKJACK:
            print("Player has Blackjack!")
        case WinStates.WIN:
            print("Player wins!")
        case WinStates.BUST:
            print("Player busts!")
        case WinStates.LOSE:
            print("Dealer wins!")
        case WinStates.PUSH:
            print("Push!")
        case _:
            print("Error: Invalid win state.")
            input("Press Enter to quit.")
            quit()

# TODO: reveal dealer's hand when ... 
def round_end(player_hand, dealer_hand, dealer_hidden):
    # print player's and dealer's hand
    clear()
    turn_state = win_state(player_hand, dealer_hand)
    print("Round ends. Cards left: %s of %s\n" %(len(deck), max_deck))
    if turn_state != None:
        print_hands(player_hand, dealer_hand, dealer_hidden = False)
        win_message(turn_state)
        input("Press Enter to quit.")
        quit()
    else:
        print_hands(player_hand, dealer_hand, dealer_hidden = True)
        input("Press Enter to continue.")

def player_turn(player_hand, dealer_hand):
    player_score = calc_score(player_hand)
    print_hands(player_hand, dealer_hand, dealer_hidden=True)

    question = f"Do you want to {textDecorations.UNDERLINE}H{textDecorations.END}it or {textDecorations.UNDERLINE}S{textDecorations.END}tand? "
    while player_score < 21:
        choice = input(question).upper()
        # sanity check for player's choice
        allowed_choices = ["H", "S"]
        if choice not in allowed_choices:
            print_hands(player_hand, dealer_hand)
            print(f"Input '{choice}' is invalid.")
            
        # if player chooses to hit
        if choice == "H":
            print("Player decided to hit.")
            # deal random card to player
            player_card = deal_card(deck, player_hand)

            # update player's score
            player_score += player_card.value

            # update player's score if player has Ace
            c = 0
            while player_score > 21 and c < len(player_hand):
                if player_hand[c].value == 11:
                    player_hand[c].value = 1
                    player_score -= 10
                c += 1

            # print player's and dealer's hand
            print_hands(player_hand, dealer_hand)
            
        # if player chooses to stand
        elif choice == "S":
            print("Player decided to stand.")
            break

    input("Press Enter to continue.")

def dealer_turn(player_hand, dealer_hand):
    dealer_score = calc_score(dealer_hand)
    while dealer_score < DEALER_STANDS:
        print("Dealer decided to hit.")

        # deal random card to dealer
        dealer_card = deal_card(deck, dealer_hand)
        
        # update dealer's score
        dealer_score += dealer_card.value

        # update dealer's score if dealer has Ace
        c = 0
        while dealer_score > 21 and c < len(dealer_hand):
            if dealer_hand[c].value == 11:
                dealer_hand[c].value = 1
                dealer_score -= 10
            c += 1

        print_hands(player_hand, dealer_hand)

    
    # dealer's score is greater than or equal to 17
    print("Dealer stands.")
    input("Press Enter to continue.")

def print_hand(hand, dealer_hidden=True):
    # print cards in hand
    for card in hand:
        if dealer_hidden and card == hand[1]:
            print("Hidden")
        else:
            print_card(card)

def print_card(card):
    print(f"{card.rank}{card.suit}")

def print_hands(player_hand, dealer_hand, dealer_hidden=True):
    player_score = calc_score(player_hand)
    dealer_score = calc_score(dealer_hand)
    clear()
    # print player's hand and score
    print(f"{textDecorations.GREEN}Player Hand:{textDecorations.END} ")
    print_hand(player_hand, False)
    print("Player Score: ", player_score)
    # print player status (blackjack, bust, stand)
    print()
    # print dealer's hand and score
    print(f"{textDecorations.RED}Dealer Hand:{textDecorations.END}")
    print_hand(dealer_hand, dealer_hidden)
    print("Dealer Score: ", dealer_score - dealer_hand[1].value if dealer_hidden else dealer_score)
    # print dealer status (blackjack, bust, stand)
    print()


if __name__ == "__main__":
    # suits and icons
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    suit_icons = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}

    # ranks and values
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    rank_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    DECKS_USED = 6
    deck = []
    
    # Creating the deck of cards
    for i in range(DECKS_USED):
        for suit in suits:
            for card in ranks:
                deck.append(Card(suit_icons[suit], card, rank_values[card]))
    
    max_deck = len(deck)
    blackjack_game(deck)