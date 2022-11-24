from itertools import chain

from flask import Flask
from tinyhtml import _h, html, h

import games
import players
import scoreboard
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


@app.route("/live")
def live_ttfl_scores():
    scoreboards = scoreboard.scoreboard_links()
    ps = list(chain(*[scoreboard.players_ttfl_score(s) for s in scoreboards]))
    ps_sorted = sorted(ps, key=lambda x: x[1], reverse=True)

    return html()(
        h("style")("table, th, td { border: 1px solid black; }"),
        h("head")(h("meta", charset="utf-8")),
        h("body")(
            h("div")(
                h("table")(
                    h("tr")(
                        h("th")("Joueur"),
                        h("th")("Score TTFL"),
                        h("th")("Temps")
                    ),
                    (h("tr")(
                        h("td")(pss[0]),
                        h("td")(pss[1]),
                        h("td")(pss[2]),
                    ) for pss in ps_sorted)
                )
            )
        )
    ).render()


def html_gamelog(gamelog_for_player: list[tuple[Player, Gamelog]]) -> _h:
    sorted_by_ttfl_average: list[tuple[Player, Gamelog]] = sorted(
        gamelog_for_player,
        key=lambda t: t[1].ttfl_average,
        reverse=True
    )

    return html()(
        h("style")("table, th, td { border: 1px solid black; }"),
        h("head")(h("meta", charset="utf-8")),
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
                h("th")("Minutes jouées"),
                h("th")("Score TTFL"),
            ),
            (h("tr")(
                h("td")(result.date.strftime("%d-%m-%Y")),
                h("td")(result.opponent.value[1]),
                h("td")(result.location.value),
                h("td")(f"{result.minutes_played}"),
                h("td")(result.ttfl_stats.score)
            ) for result in gamelog.entries)
        )
    )
