from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from parser import Parser
from fsm import HandFSM

app = Flask(__name__)

# Allow all origins, allow credentials, and handle OPTIONS preflight
CORS(app, supports_credentials=True)

@app.route("/data", methods=["GET"])
def data():
    with open("example_game.json", "r") as f:
        game = json.load(f)
    return jsonify(Parser.get_everything(game))

@app.route("/start_game", methods=["POST", "OPTIONS"])  # add OPTIONS here
def start_game():
    if request.method == "OPTIONS":
        # Preflight request, return only headers
        return '', 200

    data = request.get_json()
    print("Received start_game data:", data)

    game_dict = {
        "meta": {
            "players": {str(i): p for i, p in enumerate(data.get("players", []))},
            "small_blind": data.get("smallBlind"),
            "big_blind": data.get("bigBlind"),
            "buy_in": data.get("buyIn"),
        },
        "hands": []
    }

    fsm = HandFSM(game_dict)
    fsm.run()

    return jsonify({"status": "ok"})
