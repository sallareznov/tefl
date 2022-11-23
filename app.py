from tinyhtml import _h, html, h

from player_gamelog import matching_players, gamelog
from players import Player

from flask import Flask

from players_db import get_players_from_db

app = Flask(__name__)

all_players = get_players_from_db()


@app.route("/gamelog/<substring>")
def player_gamelog(substring):
    assert substring.__len__() >= 3
    players: list[Player] = matching_players(all_players, substring)
    return html_gamelog(players).render()


def html_gamelog(players: list[Player]) -> _h:
    return html()(
        h("style")("table, th, td { border: 1px solid black; }"),
        h("body")(
            (h("div")(
                h("h2")(player.name),
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
                        h("td")(result.ttfl_bonus),
                        h("td")(result.ttfl_malus),
                        h("td")(result.ttfl_score)
                    ) for result in gamelog(player))
                )
            ) for player in players)
        )
    )
