import unittest
from unittest.mock import patch
from deck import Deck
from card import suits

class TestDeck(unittest.TestCase):
    def test_init(self):
        # GIVEN
        # WHEN
        deck = Deck()

        # THEN
        self.assertEqual(len(deck.cards), 36, "Amount of cards should be 36")

    def test_shuffle(self):
        # GIVEN
        with patch("random.shuffle") as mock_shuffle:
            # WHEN
            deck = Deck()

            # THEN
            mock_shuffle.assert_called_once_with(deck.cards)

    def test_cards(self):
        # GIVEN
        # WHEN
        deck = Deck()

        # THEN
        for card in deck.cards:
            self.assertTrue(card.suit in suits, f"Card suit should be one of {suits}")
            self.assertTrue(card.rank >= 6 and card.rank <= 14, "Card rank should be 6 or higher")