from deck import Deck
from card import Card, rank_to_str
from player import Player
import random
import json

MAX_INITIAL_CARDS = 6

class GameController():
    def __init__(self):
        self.deck = Deck()
        self.players: list[Player] = [Player("Oleg"), Player("Bob", is_bot=True)]
        self.table: list[Card] = []
        self.discard_pile: list[Card] = []
        self.main_suit = None
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
        self.main_suit = self.deck.cards[len(self.deck.cards) - 1].suit

        # Шукаємо найменший козир кожного гравця
        min_main_suits = {}
        for player in self.players:
            main_suits_cards = []
            for card in player.cards:
                if card.suit == self.main_suit:
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
            for player, min in min_main_suits.items():
                if min < current_min:
                    current_min = min
                    self.current_player = player

            current_min_str = rank_to_str(current_min)
            print(f"{self.current_player}, {current_min_str} of {self.main_suit}")

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

    def play_card(self, card: Card):
        if len(self.table) == 0:
            self.current_player.cards.pop(selected_card_index - 1)
            
            # Походити
            self.table.append(selected_card)

            # TODO: Добавити розумніший вибір наступного гравця
            self.current_player = self.players[1]
        else:
            print(f"[T]: Зняти карти")
            card_beaten = False
            while not card_beaten:
                # Вибір карти
                selection = input("Виберіть карту або напишіть T, щоб зняти карти: ")
                if selection == "T":
                    # Зняти карти
                    self.current_player.cards.extend(self.table)

                    # Очистити стіл від карт
                    self.table.clear()

                    # TODO: Добавити розумніший вибір наступного гравця
                    self.current_player = self.players[1]
                    break
                
                selected_card_index = int(selection)
                selected_card = self.current_player.cards[selected_card_index - 1]
                print("Ви вибрали", selected_card)

                if selected_card.can_beat(self.table[0], self.main_suit):
                    # Побити карту
                    card_beaten = True
                    card = self.current_player.cards.pop(selected_card_index - 1)
                    self.table.append(card)

                    # Викинути карти у відбій
                    self.discard_pile.extend(self.table)
                    self.table.clear()
                else:
                    print("Select other card")


    def other(self):
        # Стіл має поточні карти під час ходу
        table: list[Card] = []
        # Відбій карт
        discard_pile: list[Card] = []

        # Початок гри
        while not self.is_game_over(self.players, self.deck):
            # Взяти бракуючу кількість карт з колоди для кожного гравця
            for player in self.players:
                self.take_cards(player, self.deck)
            
            print("Current table:", table)
            if current_player.is_bot:
                print("Bots turn")
                print(f"Bots cards {current_player.cards}")

                if len(table) > 0:
                    card_beaten = False
                    for index, card in enumerate(current_player.cards):
                        if card.can_beat(table[0], self.main_suit):
                            print(f"Bot beats with {card}")

                            # Побити карту
                            card_beaten = True
                            table.append(card)
                            del current_player.cards[index]

                            # Викинути карти у відбій
                            discard_pile.extend(table)
                            table.clear()
                            break
                    
                    if not card_beaten:
                        # Зняти карти
                        current_player.cards.extend(table)
                        
                        # Очистити стіл від карт
                        table.clear()

                        # TODO: Добавити розумніший вибір наступного гравця
                        current_player = self.players[0]
                        continue

                # Вибираємо випадкову карту
                selected_card_index = random.randint(0, len(current_player.cards) - 1)
                selected_card = current_player.cards.pop(selected_card_index)
                print("Bot selected", selected_card)

                table.append(selected_card)

                # TODO: Добавити розумніший вибір наступного гравця
                current_player = self.players[0]
            else:
                self.play_card(card)
        print("GAME OVER!")
        for player in self.players:
            if len(player.cards) > 0:
                print(f"Player {player} is DUREN!")