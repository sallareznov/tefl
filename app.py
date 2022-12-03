from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import chain

import requests
from bs4 import BeautifulSoup
from flask import Flask
from pytz import timezone
from tinyhtml import _h, html, h, raw

import gamelog
import injury_reports
import scoreboard
import scores
from emojis import Emoji
from games import Gamelog
from injury_reports import PlayerInjuryStatus, TeamInjuryReport
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
        h("head")(head),
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


@app.route("/injuries")
def injury_report():
    url = latest_injury_report_url()
    today = datetime.now(timezone("US/Eastern"))
    reports = injury_reports.get_injury_reports(url, today)

    return html()(
        h("head")(head),
        h("body")(
            h("div")(
                h("h2")("Injury Report"),
                h("table", klass="table table-responsive table-bordered")(
                    h("thead", klass="table-light")(
                        h("tr")(
                            h("th", klass="text-center", bgcolor="gray", scope="col")("#"),
                            h("th", klass="text-center", bgcolor="gray", scope="col")("Équipe"),
                            h("th", klass="text-center", bgcolor="gray", scope="col")("Adversaire"),
                            injury_status_header("#007500", "PROBABLE", "(80% de chances de jouer)"),
                            injury_status_header("#778A35", "QUESTIONABLE", "(50% de chances de jouer)"),
                            injury_status_header("#A35900", "DOUBTFUL", "(25% de chances de jouer)"),
                            injury_status_header("#8B0903", "OUT", "(0% de chances de jouer)")
                        )
                    ),
                    h("tbody", klass="table-group-divider")(
                        h("tr")(
                            h("th", scope="row")(index + 1),
                            h("td")(h("img", src=report.team.logo()), f" {report.team.full_name()}"),
                            h("td", klass="text-center")(
                                h("span")(f"{report.location.value[1]} "),
                                h("img", src=report.opponent.logo())
                            ),
                            html_cell_for_injury_status(report, PlayerInjuryStatus.PROBABLE),
                            html_cell_for_injury_status(report, PlayerInjuryStatus.QUESTIONABLE),
                            html_cell_for_injury_status(report, PlayerInjuryStatus.DOUBTFUL),
                            html_cell_for_injury_status(report, PlayerInjuryStatus.OUT)
                        ) for index, report in enumerate(reports))
                )
            )
        )
    ).render()


def injury_status_header(bg_color: str, title: str, description: str) -> _h:
    return h("th", klass="text-center", scope="col", style="color:white;", bgcolor=bg_color)(
        h("span", style="font-weight:bold;")(title), h("br"), h("span")(description),
    )


def html_cell_for_injury_status(report: TeamInjuryReport, status: PlayerInjuryStatus) -> _h:
    return h("td", klass="text-center")(
        raw(f"{player.name}<br>") for player in report.players_with_status(status)
    )


def latest_injury_report_url() -> str:
    response = requests.get("https://official.nba.com/nba-injury-report-2022-23-season/")
    soup = BeautifulSoup(response.text, "html.parser")
    injury_reports = soup.select("div[class~=post-injury] a")

    return [report.get("href") for report in injury_reports][-1]


def html_gamelog(gamelog_for_player: list[tuple[Player, Gamelog]]) -> _h:
    sorted_by_ttfl_average: list[tuple[Player, Gamelog]] = sorted(
        gamelog_for_player,
        key=lambda t: t[1].ttfl_average,
        reverse=True
    )

    return html()(
        h("head")(head),
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
                        h("span", style="font-weight:bold;")(result.ttfl_stats.score),
                        scores.to_emoji(result.ttfl_stats.score).html()
                    )
                ) for (index, result) in enumerate(g.entries))
            )
        )
    )


head = (
    h("meta", charset="utf-8"),
    h("link", rel="stylesheet",
      href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
      integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm",
      crossorigin="anonymous"
      ),
    h("link", rel="icon", href="https://download.vikidia.org/vikidia/fr/images/7/7a/Basketball.png")
)

#if __name__ == '__main__':
#    hti = Html2Image()
#    hti.screenshot(url='http://127.0.0.1:5000/injuries', save_as='python_org.png')
