from card import Card, suits
import random

class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        self.__generatedeck__()
        random.shuffle(self.cards)

    def __generatedeck__(self):
        for suit in suits:
            for rank in range(2, 15):
                card = Card(suit, rank)
                self.cards.append(card)