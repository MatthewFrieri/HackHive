from flask import Flask, jsonify
from flask_cors import CORS
import json

from parser import Parser

app = Flask(__name__)
CORS(app)

@app.route("/data")
def data():
    f = open("example_game.json", "r")
    game = json.load(f)
    return jsonify(Parser.get_everything(game))
