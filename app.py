from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask
from pytz import timezone
from tinyhtml import _h, html, h, raw

import gamelog
import injury_reports
import live_scores
import players
from games import Gamelog, GameLocation
from injury_reports import PlayerInjuryStatus, TeamInjuryReport, TeamInjuryReportStatus
from players import Player
from players_db import get_players_from_db
from teams import Team

app = Flask(__name__)

all_players = get_players_from_db()


@app.route("/")
def home():
    return html()(
        h("head")(head),
        h("body")(
            h("div", klass="list-group")(
                list_item("/live", "Live scores", "Scores TTFL en live de la soirée"),
                list_item("/injuries", "Injury report", "Injury report le plus récent des matchs de la soirée")
            )
        )
    ).render()


def list_item(href: str, title: str, description: str) -> _h:
    return h("a", href=href, klass="list-group-item list-group-item-action flex-column align-items-start")(
        h("div", klass="d-flex w-100 justify-content-between")(
            h("h5", klass="mb-1")(title)
        ),
        h("p", klass="mb-1")(description)
    )


@app.route("/gamelog/<search>")
def player_ttfl_gamelog(search: str):
    assert search.__len__() >= 2
    matching_players = players.matching_players(search, all_players)
    gamelog_for_player = [(player, gamelog.compute_gamelog(player)) for player in matching_players]

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
    ).render()


@app.route("/live")
def live_ttfl_scores():
    all_scores = live_scores.live_ttfl_scores()

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
                            h("th", scope="col")("Adversaire"),
                            h("th", scope="col", klass="text-center")("Minutes jouées"),
                            h("th", scope="col", klass="text-center")("Terrain/Banc?"),
                            h("th", scope="col", klass="text-center")("Temps du match"),
                            h("th", scope="col", klass="text-center")("Score du match"),
                        )
                    ),
                    h("tbody", klass="table-group-divider")(
                        h("tr")(
                            h("th", scope="row")(index + 1),
                            h("td")(player_score.name_html()),
                            h("td", klass="text-center")(player_score.ttfl_score_html()),
                            h("td")(player_score.opponent_team_html()),
                            h("td", klass="text-center")(player_score.minutes_played_html()),
                            h("td", klass="text-center")(player_score.on_court_emoji().html()),
                            h("td", klass="text-center")(player_score.game_status),
                            h("td", klass="text-center")(player_score.game_score_html())
                        ) for index, player_score in enumerate(all_scores)
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
                        team_injury_report(index, report) for index, report in enumerate(reports)
                    )
                )
            )
        )
    ).render()


def injury_status_header(bg_color: str, title: str, description: str) -> _h:
    return h("th", klass="text-center", scope="col", style="color:white;", bgcolor=bg_color)(
        h("span", style="font-weight:bold;")(title), h("br"), h("span")(description),
    )


def team_injury_report(index: int, report: TeamInjuryReport) -> _h:
    match report.status:
        case TeamInjuryReportStatus.SUBMITTED:
            return h("tr")(
                h("th", scope="row")(index + 1),
                h("td")(report.team.html_with_full_name()),
                h("td", klass="text-center")(matchup_html(report.location, report.opponent)),
                report.html_cell_for_injury_status(PlayerInjuryStatus.PROBABLE),
                report.html_cell_for_injury_status(PlayerInjuryStatus.QUESTIONABLE),
                report.html_cell_for_injury_status(PlayerInjuryStatus.DOUBTFUL),
                report.html_cell_for_injury_status(PlayerInjuryStatus.OUT)
            )
        case TeamInjuryReportStatus.NOT_YET_SUBMITTED:
            return h("tr", bgcolor="#C0C0C0")(
                h("th", scope="row")(index + 1),
                h("td")(report.team.html_with_full_name()),
                h("td", klass="text-center")(matchup_html(report.location, report.opponent)),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ")
            )


def matchup_html(location: GameLocation, opponent: Team): return location.html_with_text(), " ", opponent.logo_html()


def html_cell_for_injury_status(report: TeamInjuryReport, status: PlayerInjuryStatus):
    return h("td", klass="text-center")(
        raw(f"{player.name}<br>") for player in report.players_with_status(status)
    )


def latest_injury_report_url() -> str:
    response = requests.get("https://official.nba.com/nba-injury-report-2022-23-season/")
    soup = BeautifulSoup(response.text, "html.parser")
    injury_reports = soup.select("div[class~=post-injury] a")

    return [report.get("href") for report in injury_reports][-1]


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
                h("tr")(
                    h("th", scope="row")(index + 1),
                    h("td")(result.date.strftime("%d-%m-%Y")),
                    h("td")(result.opponent.html_with_nickname()),
                    h("td", klass="text-center")(result.location.html_with_emoji()),
                    h("td", klass="text-center")(result.minutes_played_html()),
                    h("td", klass="text-center")(result.ttfl_stats.html())
                ) for (index, result) in enumerate(g.entries)
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
