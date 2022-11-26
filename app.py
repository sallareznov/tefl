from concurrent.futures import ThreadPoolExecutor
from itertools import chain

from flask import Flask
from tinyhtml import _h, html, h

import emojis
import gamelog
import scoreboard
from emojis import Emoji
from games import Gamelog
from players import Player
from players_db import get_players_from_db

app = Flask(__name__)

all_players = get_players_from_db()


@app.route("/gamelog/<search>")
def player_ttfl_gamelog(search: str):
    assert search.__len__() >= 3
    matching_players = gamelog.matching_players(all_players, search)
    gamelog_for_player = [(player, gamelog.compute_gamelog(player)) for player in matching_players]
    return html_gamelog(gamelog_for_player).render()


@app.route("/live")
def live_ttfl_scores():
    scoreboards = scoreboard.scoreboard_links()
    performances = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        for result in executor.map(scoreboard.ttfl_scores_for_game, [s for s in scoreboards]):
            performances.append(result)

    performances_sorted_by_ttfl_score = sorted(list(chain(*performances)), key=lambda perf: perf[1], reverse=True)

    return html()(
        h("head")(
            h("meta", charset="utf-8"),
            h(
                "link",
                rel="stylesheet",
                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm",
                crossorigin="anonymous"
            )
        ),
        h("body")(
            h("div")(
                h("h2")("Meilleurs scores TTFL de la nuit"),
                h("table", klass="table table-sm table-responsive table-bordered")(
                    h("thead", klass="table-light")(
                        h("tr")(
                            h("th", scope="col")("#"),
                            h("th", scope="col")("Joueur"),
                            h("th", scope="col", klass="text-center")("Score TTFL"),
                            h("th", scope="col", klass="text-center")("Minutes jouées"),
                            h("th", scope="col", klass="text-center")("Adversaire")
                        )
                    ),
                    h("tbody", klass="table-group-divider")(
                        h("tr")(
                            h("th", scope="row")(index + 1),
                            h("td")(h("img", src=team.logo()), f" {player}"),
                            h("td", klass="text-center")(h("span", style="font-weight:bold;")(score)),
                            h("td", klass="text-center")(f" {minutes}", Emoji.stopwatch.html()),
                            h("td", klass="text-center")(location.value[1].html(), f" {opponent.value[1]}")
                        ) for index, (player, score, minutes, team, location, opponent) in
                        enumerate(performances_sorted_by_ttfl_score)
                    )
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
        h("head")(
            h("meta", charset="utf-8"),
            h(
                "link",
                rel="stylesheet",
                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm",
                crossorigin="anonymous"
            )
        ),
        h("body")(
            (single_player_gamelog(player) for player in sorted_by_ttfl_average)
        )
    )


def single_player_gamelog(gamelog_for_player: tuple[Player, Gamelog]):
    (p, g) = gamelog_for_player

    return h("div")(
        h("h2")(f"{p.name} [moyenne TTFL: {g.ttfl_average}]"),
        h("table", klass="table table-sm table-responsive table-bordered")(
            h("thead", klass="table-light")(
                h("tr")(
                    h("th", scope="col")("#"),
                    h("th", scope="col")("Date"),
                    h("th", scope="col")("Adversaire"),
                    h("th", scope="col")("Lieu"),
                    h("th", scope="col")("Minutes jouées"),
                    h("th", scope="col")("Score TTFL")
                )
            ),
            h("tbody", klass="table-group-divider")(
                (h("tr")(
                    h("th", scope="row")(index + 1),
                    h("td")(result.date.strftime("%d-%m-%Y")),
                    h("td")(
                        h("img", src=result.opponent.logo()),
                        f" {result.opponent.value[1]}"
                    ),
                    h("td")(result.location.html()),
                    h("td", klass="text-center")(
                        f"{result.minutes_played}",
                        h("span")(Emoji.stopwatch.html())
                    ),
                    h("td", klass="text-center")(
                        result.ttfl_stats.score,
                        emojis.from_ttfl_score(result.ttfl_stats.score).html()
                    )
                ) for (index, result) in enumerate(g.entries))
            )
        )
    )



