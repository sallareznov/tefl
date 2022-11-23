from flask import Flask
from tinyhtml import _h, html, h

import games
import players
from games import Gamelog
from players import Player
from players_db import get_players_from_db

app = Flask(__name__)

all_players = get_players_from_db()


@app.route("/gamelog/<search>")
def player_ttfl_gamelog(search: str):
    assert search.__len__() >= 3
    matching_players = players.matching_players(all_players, search)
    gamelog_for_player = [(player, games.gamelog(player)) for player in matching_players]
    return html_gamelog(gamelog_for_player).render()


def html_gamelog(gamelog_for_player: list[tuple[Player, Gamelog]]) -> _h:
    sorted_by_ttfl_average: list[tuple[Player, Gamelog]] = sorted(
        gamelog_for_player,
        key=lambda t: t[1].ttfl_average,
        reverse=True
    )

    return html()(
        h("style")("table, th, td { border: 1px solid black; }"),
        h("body")(
            (h("div")(single_player_gamelog(player)) for player in sorted_by_ttfl_average)
        )
    )


def single_player_gamelog(gamelog_for_player: tuple[Player, Gamelog]):
    (player, gamelog) = gamelog_for_player
    return h("div")(
        h("h2")(f"{player.name} [moyenne TTFL: {gamelog.ttfl_average}] [{gamelog.games_played} matchs joués]"),
        h("table")(
            h("tr")(
                h("th")("Date"),
                h("th")("Adversaire"),
                h("th")("Lieu"),
                h("th")("Score TTFL"),
            ),
            (h("tr")(
                h("td")(result.date.strftime("%d-%m-%Y")),
                h("td")(result.opponent.value[1]),
                h("td")(result.location.value),
                h("td")(result.ttfl_stats.score)
            ) for result in gamelog.entries)
        )
    )
