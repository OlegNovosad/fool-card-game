from card import Card

class Player:
    def __init__(self, name: str, cards: list[Card] = [], is_bot: bool = False):
        self.name = name
        self.cards = cards
        self.is_bot = is_bot

    def __str__(self):
        if self.is_bot:
            return f"{self.name} [bot]"
        else:
            return f"{self.name}"
        
    def __repr__(self) -> str:
        if self.is_bot:
            return f"{self.name} [bot]"
        else:
            return f"{self.name}"