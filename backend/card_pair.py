from card import Card

class CardPair:
    """
        `played_card` is the card which was played by user
        `beaten_card` is the card that played card was beated with
    """
    def __init__(self, played_card: Card, beaten_card: Card = None):
        self.played_card = played_card
        self.beaten_card = beaten_card