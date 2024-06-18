import random
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


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

    # Phase 1: Deal 2 cards to player and dealer
    while len(player_hand) < 2:
        # deal random card to player
        player_card = random.choice(deck)
        player_hand.append(player_card)
        deck.remove(player_card)
        
        player_score += player_card.value

        # Check for double Ace
        if(len(player_hand) == 2):
            if player_hand[0].value == "11" and player_hand[1].value == "A":
                player_hand[0].value = "1"
                player_score -= 10
        
        # Print player hand
        print("Player Hand: ")
        print_hand(player_hand, False)
        print("Player Score: ", player_score)

        input()

    while len(dealer_hand) < 2:
        # deal random card to dealer
        dealer_card = random.choice(deck)
        dealer_hand.append(dealer_card)
        deck.remove(dealer_card)

        # update dealer's score
        dealer_score += dealer_card.value

        # Print dealer hand
        if(len(dealer_hand) == 1):
            print("Dealer Hand: ")
            print_hand(dealer_hand, False)
            print("Dealer Score: ", dealer_score)
        else:
            print("Dealer Hand: ")
            print_hand(dealer_hand, True)
            print("Dealer Score: ", dealer_score - dealer_hand[1].value)

        # Check for double Ace
        if(len(dealer_hand) == 2):
            if dealer_hand[0].value == "11" and dealer_hand[1].value == "A":
                dealer_hand[1].value = "1"
                dealer_score -= 10

        input()

    # Check for Blackjack
    if(player_score == 21):
        print("PLAYER HAS BLACKJACK!")
        print("PLAYER WINS!")
        quit()

    clear()

    # print player's and dealer's hand
    print_hands(player_hand, dealer_hand, player_score, dealer_score)

# Phase 2: Player's Turn
    # managing player's turn
    while player_score < 21:
        choice = input("Do you want to (H)it or (S)tand? ").upper()
        # sanity check for player's choice
        if len(choice) != 1 or choice != "H" and choice != "S":
            clear()
            print("Invalid choice. Do you want to (H)it or (S)tand? ")
            
        # if player chooses to hit
        if choice == "H":
            # deal random card to player
            player_card = random.choice(deck)
            player_hand.append(player_card)
            deck.remove(player_card)

            # update player's score
            player_score += player_card.value

            # update player's score if player has Ace
            c = 0
            while player_score > 21 and c < len(player_hand):
                if player_hand[c].value == 11:
                    player_hand[c].value = 1
                    player_score -= 10
                c += 1
            
            clear()
            
            # print player's and dealer's hand
            print_hands(player_hand, dealer_hand, player_score, dealer_score)
            
        # if player chooses to stand
        elif choice == "S":
            break

    clear()
    
    # print player's and dealer's hand
    print_hands(player_hand, dealer_hand, player_score, dealer_score, False)

    # check if player's has blackjack
    if player_score == 21:
        print("PLAYER HAS BLACKJACK!")
        print("PLAYER WINS!")
        quit()

    # check if player's score is greater than 21
    if player_score > 21:
        print("PLAYER BUSTS!")
        print("DEALER WINS!")
        quit()

    input()
    
# Phase 3: Dealer's Turn
    # managing dealer's turn
    # dealer's score is less than 17
    while dealer_score < 17:
        clear()

        print("Dealer decides to hit.")

        # deal random card to dealer
        dealer_card = random.choice(deck)
        dealer_hand.append(dealer_card)
        deck.remove(dealer_card)

        # update dealer's score
        dealer_score += dealer_card.value

        # update dealer's score if dealer has Ace
        c = 0
        while dealer_score > 21 and c < len(dealer_hand):
            if dealer_hand[c].value == 11:
                dealer_hand[c].value = 1
                dealer_score -= 10
            c += 1
        
        # print player's and dealer's hand
        print_hands(player_hand, dealer_hand, player_score, dealer_score, False)
    
# Phase 4: Compare player's and dealer's score
    # if dealer has blackjack
    if dealer_score == 21:
        print("DEALER HAS BLACKJACK!")
        print("DEALER WINS!")
        quit()
    
    # if dealer's score is greater than 21
    elif dealer_score > 21:    
        print("DEALER BUSTS!")
        print("PLAYER WINS!")
        quit()
    
    # if player's score is equal to dealer's score
    elif dealer_score == player_score:
        print("IT'S A TIE!")
    
    # if player's score is greater than 21
    if player_score > dealer_score:
        print("PLAYER HAS HIGHER SCORE!")
        print("PLAYER WINS!")
    
    # Dealer wins
    else:
        print("DEALER HAS HIGHER SCORE!")
        print("DEALER WINS!")

def print_hand(hand, hidden=True):    
    # print cards in hand
    for card in hand:
        if hidden and card == hand[1]:
            print("Hidden")
        else:
            print_card(card)

def print_card(card):
    print(f"{card.rank}{card.suit}")

def print_hands(player_hand, dealer_hand, player_score, dealer_score, hidden=True, dealer_turn=False):
    # print dealer's hand and score
    print("Dealer Hand: ")
    print_hand(dealer_hand, hidden)
    print("Dealer Score: ", dealer_score - dealer_hand[1].value if hidden else dealer_score)
    print()
    # print player's hand and score
    print("Player Hand: ")
    print_hand(player_hand)
    print("Player Score: ", player_score)



if __name__ == "__main__":
    # suits
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    
    # suits values
    suit_icons = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}

    # ranks
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    # values
    rank_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    # The deck of cards
    deck = []

    # Loop for every type of suit
    for suit in suits:
 
        # Loop for every type of card in a suit
        for card in ranks:
 
            # Adding card to the deck
            deck.append(Card(suit_icons[suit], card, rank_values[card]))
     
    blackjack_game(deck)