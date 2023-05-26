from deck import Deck
from card import Card, rank_to_str
from player import Player
from card_pair import CardPair
import random

MAX_INITIAL_CARDS = 6

class GameController():
    def __init__(self):
        # Колода
        self.deck = Deck()

        # Список гравців
        self.players: list[Player] = [Player("Bob", is_bot=True)]

        # Список гравців, які вже ходили
        self.already_played_players: list[Player] = []
        
        # Стіл має поточні карти під час ходу
        self.table: list[CardPair] = []

        # Відбій карт
        self.discard_pile: list[Card] = []

        # Козир (карта)
        self.trump_card = None

        # Поточний гравець
        self.current_player: Player = None

    def deal_cards(self):
        # Роздаємо карти гравцям
        for player in self.players:
            cards = []
            for i in range(MAX_INITIAL_CARDS):
                card = self.deck.cards.pop()
                cards.append(card)
                player.cards = cards

        # Визначаємо козир
        self.trump_card = self.deck.cards[len(self.deck.cards) - 1]

        # Шукаємо найменший козир кожного гравця
        min_main_suits = {}
        for player in self.players:
            main_suits_cards = []
            for card in player.cards:
                if card.suit == self.trump_card.suit:
                    main_suits_cards.append(card.rank)

            if len(main_suits_cards) > 0:
                min_main_suits[player] = min(main_suits_cards)

        # Якщо немає козирів в обидвох граців, то
        # випадковий гравець ходить першим
        if len(min_main_suits) == 0:
            index = random.randint(0, len(self.players) - 1)
            self.current_player = self.players[index]
            print(f"{self.current_player}")
        else:
            # Шукаємо найменший козир серед усіх гравців
            current_min = list(min_main_suits.values())[0]
            self.current_player = list(min_main_suits.keys())[0]
            for player, player_min in min_main_suits.items():
                if player_min < current_min:
                    current_min = player_min
                    self.current_player = player

            current_min_str = rank_to_str(current_min)
            print(f"{self.current_player}, {current_min_str} of {self.trump_card.suit}")

    def is_game_over(self, players: list[Player], deck: Deck):
        game_over = True

        if len(deck.cards) > 0:
            game_over = False
        else:
            players_left = 0
            for player in players:
                if len(player.cards) > 0:
                    players_left += 1

            if players_left > 1:
                game_over = False

        return game_over

    def take_cards(self, player: Player, deck: Deck):
        while len(player.cards) < MAX_INITIAL_CARDS:
            card = deck.cards.pop()
            player.cards.append(card)

    def replenish_cards(self):
        # Взяти бракуючу кількість карт з колоди для кожного гравця
        for player in self.players:
            self.take_cards(player, self.deck)

    def play_card(self, card: Card) -> bool:
        if len(self.table) == 0:
            for i, c in enumerate(self.current_player.cards):
                if c.rank == card.rank and c.suit == card.suit:
                    del self.current_player.cards[i]
                    break
            
            # Походити
            self.table.append(CardPair(played_card=card))
        else:
            # Вибір карти
            # selection = input("Виберіть карту або напишіть T, щоб зняти карти: ")
            # if selection == "T":
            #     # Зняти карти
            #     # TODO: Розпакувати карти перед зняттям (played, beaten)
            #     self.current_player.cards.extend(self.table)

            #     # Очистити стіл від карт
            #     self.table.clear()

            #     self.switch_player()
            #     break

            if card.can_beat(self.table[0].played_card, self.trump_card.suit):
                # Побити карту
                for i, c in enumerate(self.current_player.cards):
                    if c.rank == card.rank and c.suit == card.suit:
                        del self.current_player.cards[i]
                        break

                self.table.append(card)

                # Викинути карти у відбій
                self.discard_pile.extend(self.table)
                self.table.clear()
            else:
                return False
        return True


    def play_bot_card(self):
        print("Bots turn")
        print(f"Bots cards {self.current_player.cards}")

        if len(self.table) > 0:
            card_beaten = False
            for index, card in enumerate(self.current_player.cards):
                if card.can_beat(self.table[0].played_card, self.trump_card.suit):
                    print(f"Bot beats with {card}")

                    # Побити карту
                    card_beaten = True
                    # TODO: Знайти карту, яку хочемо побити
                    self.table[0].beaten_card = card
                    del self.current_player.cards[index]

                    # Викинути карти у відбій
                    # self.discard_pile.extend(self.table)
                    # self.table.clear()
                    break
            
            if not card_beaten:
                # Зняти карти
                # TODO: Розпакувати карти перед зняттям (played, beaten)
                self.current_player.cards.extend(self.table)
                
                # Очистити стіл від карт
                self.table.clear()

                self.switch_player()
            return

        # Вибираємо випадкову карту
        selected_card_index = random.randint(0, len(self.current_player.cards) - 1)
        selected_card = self.current_player.cards.pop(selected_card_index)
        print("Bot selected", selected_card)

        self.table.append(CardPair(played_card=selected_card))

        self.switch_player()

    def switch_player(self):
        self.already_played_players.append(self.current_player)

        if len(self.already_played_players) == len(self.players):
            self.already_played_players.clear()
            self.current_player = self.players[0]
        else:
            for player in self.players:
                if any(p.name != player.name for p in self.already_played_players):
                    self.current_player = player
                    break

    def other(self):
        # Початок гри
        while not self.is_game_over(self.players, self.deck):
            print("Current table:", self.table)
            if self.current_player.is_bot:
                self.play_bot_card()
            else:
                self.play_card(None)
        print("GAME OVER!")
        for player in self.players:
            if len(player.cards) > 0:
                print(f"Player {player} is DUREN!")