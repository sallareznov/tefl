from tinyhtml import _h, html, h

import games
import players
from players import Player

from flask import Flask

from players_db import get_players_from_db

app = Flask(__name__)

all_players = get_players_from_db()


@app.route("/gamelog/<search>")
def player_gamelog(search: str):
    assert search.__len__() >= 3
    p: list[Player] = players.matching_players(all_players, search)
    return html_gamelog(p).render()


def single_player_gamelog(player: Player):
    gamelog = games.gamelog(player)
    return h("div")(
        h("h2")(f"{player.name} [moyenne TTFL: {gamelog.ttfl_average}] [{gamelog.games_played} matchs joués]"),
        h("table")(
            h("tr")(
                h("th")("Date"),
                h("th")("Adversaire"),
                h("th")("Bonus TTFL"),
                h("th")("Malus TTFL"),
                h("th")("Score TTFL")
            ),
            (h("tr")(
                h("td")(result.date),
                h("td")(result.opponent),
                h("td")(result.ttfl_stats.bonus),
                h("td")(result.ttfl_stats.malus),
                h("td")(result.ttfl_stats.score)
            ) for result in gamelog.entries)
        )
    )


def html_gamelog(p: list[Player]) -> _h:
    return html()(
        h("style")("table, th, td { border: 1px solid black; }"),
        h("body")(
            (h("div")(single_player_gamelog(player)) for player in p)
        )
    )
