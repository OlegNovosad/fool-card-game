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
    player_cards = json.dumps(controller.players[0].cards, default=lambda o: o.__dict__)
    table = json.dumps(controller.table, default=lambda o: o.__dict__)
    
    emit("game-state-changed", {
        "player_cards": player_cards,
        "table": table
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
    card = Card(**data)
    controller.play_card(card)
    send_game_state()

if __name__ == "__main__":
    socketio.run(app, debug=True)