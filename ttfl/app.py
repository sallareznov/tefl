from flask import Flask
from ttfl_totals import ttfl_totals_for_player

app = Flask(__name__)


@app.route("/<player_name>")
def hello_world(player_name: str):
    return ttfl_totals_for_player(player_name).__str__()
