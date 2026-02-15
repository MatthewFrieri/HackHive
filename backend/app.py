from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from parser import Parser
from fsm import HandFSM

app = Flask(__name__)
CORS(app)

@app.route("/data", methods=["GET"])
def data():
    f = open("example_game.json", "r")
    game = json.load(f)
    return jsonify(Parser.get_everything(game))
