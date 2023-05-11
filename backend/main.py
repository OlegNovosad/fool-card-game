from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from game_controller import GameController
from card import Card
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
controller = GameController()

def send_game_state():
    players = json.dumps(controller.players, default=lambda o: o.__dict__)
    table = json.dumps(controller.table, default=lambda o: o.__dict__)
    discard_pile = json.dumps(controller.discard_pile, default=lambda o: o.__dict__)
    current_player = json.dumps(controller.current_player, default=lambda o: o.__dict__)

    emit("game-state-changed", {
        "players": json.loads(players),
        "table": json.loads(table),
        "current_player": json.loads(current_player),
        "discard_pile": json.loads(discard_pile)
    })

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    emit("connected", {"data": "Connected"})
    controller.deal_cards()
    send_game_state()

@socketio.on("disconnect")
def on_disconnect():
    emit("disconnected", {"data": "Disconnected"})

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

if __name__ == "__main__":
    socketio.run(app, debug=True)