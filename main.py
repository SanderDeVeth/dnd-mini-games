from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import os

# ... rest of your existing code (from your current main.py) ...

# Create FastAPI app
app = FastAPI(title="Blackjack Game API")

# Define a simple request model
class GameRequest(BaseModel):
    player_name: str = "Player"

@app.get("/")
def root():
    return {"message": "Welcome to the Blackjack Game API!"}

@app.post("/start-game")
def start_game(player_name: str = "Player"):
    # Initialize game state
    # You can keep your existing logic here
    deck = []
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    suit_icons = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs": "\u2667", "Diamonds": "\u2662"}
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    rank_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    DECKS_USED = 6
    for i in range(DECKS_USED):
        for suit in suits:
            for card in ranks:
                deck.append({"suit": suit_icons[suit], "rank": card, "value": rank_values[card]})

    max_deck = len(deck)
    print(f"Deck created with {max_deck} cards.")

    # Simulate game logic
    player_hand = []
    dealer_hand = []

    # Deal 2 cards
    for _ in range(2):
        card = random.choice(deck)
        player_hand.append(card)
        deck.remove(card)

    # Return initial state
    return {
        "player_name": player_name,
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "message": "Game started!"
    }