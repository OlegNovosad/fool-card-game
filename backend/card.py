suits = ["spades", "diamonds", "hearts", "clubs"]

def rank_to_str(rank: int) -> str:
    rank_str = str(rank)
    match (rank):
        case 11:
            rank_str = "J"
        case 12:
            rank_str = "Q"
        case 13:
            rank_str = "K"
        case 14:
            rank_str = "A"
    return rank_str

class Card:
    """
        Suit is one of: 
        `spades`
        `diamonds`
        `hearts`
        `clubs`

        Rank is in range: `6-14`
    """
    def __init__(self, suit: str, rank: int):
        self.suit = suit
        self.rank = rank

    def can_beat(self, other, main_suit: str) -> bool:
        result = False

        if self.suit == other.suit and self.rank > other.rank:
            result = True

        if self.suit == main_suit and other.suit != main_suit:
            result = True

        return result

    def __str__(self) -> str:
        rank = rank_to_str(self.rank)
        return f"{rank} of {self.suit}"
    
    def __repr__(self) -> str:
        rank = rank_to_str(self.rank)
        return f"{rank} of {self.suit}"