from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from game_controller import GameController
from card import Card
from player import Player
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
controller = GameController()

sessions = []

def send_game_state():
    players = json.dumps(controller.players, default=lambda o: o.__dict__)
    table = json.dumps(controller.table, default=lambda o: o.__dict__)
    discard_pile = json.dumps(controller.discard_pile, default=lambda o: o.__dict__)
    current_player = json.dumps(controller.current_player, default=lambda o: o.__dict__)
    trump_card = json.dumps(controller.trump_card, default=lambda o: o.__dict__)
    deck = json.dumps(controller.deck, default=lambda o: o.__dict__)

    emit("game-state-changed", {
        "players": json.loads(players),
        "table": json.loads(table),
        "current_player": json.loads(current_player),
        "discard_pile": json.loads(discard_pile),
        "trump_card": json.loads(trump_card),
        "deck": json.loads(deck)
    })

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    emit("connected", {"data": "Connected"})

@socketio.on("disconnect")
def on_disconnect():
    emit("disconnected", {"data": "Connected"})

@socketio.on("auth")
def on_auth(data):
    connected = data["connected"]
    name = data["name"]

    if connected == True and name not in sessions:
        sessions.append(name)
        controller.players.append(Player(name))

        controller.deal_cards()

        if controller.current_player.is_bot:
            # Хід бота
            controller.play_bot_card()

        send_game_state()
    elif connected == False and name in sessions:
        sessions.remove(name)
        controller.players = list(filter(lambda player: player.name == name, controller.players))
    else:
        send_game_state()

@socketio.on("play-card")
def on_play_card(data):
    # Хід гравця
    card = Card(**data)
    controller.play_card(card)
    send_game_state()
    
    # TODO: Перемикання гравця
    # Хід бота
    controller.play_bot_card()
    send_game_state()

    controller.replenish_cards()
    send_game_state()

if __name__ == "__main__":
    socketio.run(app)