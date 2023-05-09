from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from game_controller import GameController
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
controller = GameController()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def on_connect():
    emit("connected", {"data": "Connected"}, broadcast=True)
    
    # controller.deal_cards()

    # response = json.dumps(controller.players[0].cards, default=lambda o: o.__dict__)
    
    # emit("game-started", {
    #     "player_cards": response
    # })

@socketio.on("disconnect")
def on_disconnect():
    emit("disconnected", {"data": "Disconnected"}, broadcast=True)

@socketio.on("play-card")
def on_play_card(data):
    print(data)

if __name__ == "__main__":
    socketio.run(app, debug=True)