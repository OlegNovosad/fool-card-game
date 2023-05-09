from card import Card, suits
import random

class Deck:
    cards: list[Card] = []

    def __init__(self):
        self.__generatedeck__()
        random.shuffle(self.cards)

    def __generatedeck__(self):
        for suit in suits:
            for rank in range(2, 15):
                card = Card(suit, rank)
                self.cards.append(card)