from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask
from pytz import timezone
from tinyhtml import _h, html, h, raw

import gamelog
import injury_reports
import live_scores
import urls
from emojis import Emoji
from games import Gamelog, GameLocation
from injury_reports import PlayerInjuryStatus, TeamInjuryReport, TeamInjuryReportStatus
from players_db import get_players_from_db
from save_players_to_db import PlayerInfo
from teams import Team

app = Flask(__name__)

all_players = get_players_from_db()


@app.route("/gamelog/<search>")
def player_ttfl_gamelog(search: str):
    assert search.__len__() >= 2
    matching_players = gamelog.matching_players(search, all_players)
    gamelog_for_player = [(player, gamelog.compute_gamelog(player)) for player in matching_players]

    sorted_by_ttfl_average: list[tuple[PlayerInfo, Gamelog]] = sorted(
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
    if report.state == TeamInjuryReportStatus.SUBMITTED:
        return h("tr")(
            h("th", scope="row")(index + 1),
            h("td")(report.team.html_with_full_name()),
            h("td", klass="text-center")(matchup_html(report.location, report.opponent)),
            html_cell_for_injury_status(report, PlayerInjuryStatus.PROBABLE),
            html_cell_for_injury_status(report, PlayerInjuryStatus.QUESTIONABLE),
            html_cell_for_injury_status(report, PlayerInjuryStatus.DOUBTFUL),
            html_cell_for_injury_status(report, PlayerInjuryStatus.OUT)
        )
    else:
        return h("tr", bgcolor="#C0C0C0")(
            h("th", scope="row")(index + 1),
            h("td")(report.team.html_with_full_name()),
            h("td", klass="text-center")(matchup_html(report.location, report.opponent)),
            h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
            h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
            h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
            h("td", klass="text-center")("PAS ENCORE PUBLIÉ")
        )


def matchup_html(location: GameLocation, opponent: Team): h("span")(f"{location.value[1]} "), opponent.logo()


def html_cell_for_injury_status(report: TeamInjuryReport, status: PlayerInjuryStatus) -> _h:
    return h("td", klass="text-center")(
        raw(f"{player.name}<br>") for player in report.players_with_status(status)
    )


def latest_injury_report_url() -> str:
    response = requests.get(urls.injury_report)
    soup = BeautifulSoup(response.text, "html.parser")
    injury_reports = soup.select("div[class~=post-injury] a")

    return [report.get("href") for report in injury_reports][-1]


def single_player_gamelog(gamelog_for_player: tuple[PlayerInfo, Gamelog]):
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
                    h("td", klass="text-center")(result.location.html()),
                    h("td", klass="text-center")(minutes_played_html(result.minutes_played)),
                    h("td", klass="text-center")(ttfl_score_html_with_emoji(result.ttfl_stats.score))
                ) for (index, result) in enumerate(g.entries)
            )
        )
    )


def minutes_played_html(minutes_played: int):
    return f"{minutes_played} ", h("span")(Emoji.stopwatch.html())


def ttfl_score_html_with_emoji(ttfl_score: int):
    return h("span", style="font-weight:bold;")(ttfl_score), score_to_emoji(ttfl_score).html()


def score_to_emoji(ttfl_score: int) -> Emoji:
    match ttfl_score:
        case _ if ttfl_score < 10:
            return Emoji.face_vomiting
        case _ if ttfl_score < 20:
            return Emoji.expressionless
        case _ if ttfl_score < 30:
            return Emoji.face_with_rolling_eyes
        case _ if ttfl_score < 35:
            return Emoji.unamused
        case _ if ttfl_score < 40:
            return Emoji.sweat_smile
        case _ if ttfl_score < 45:
            return Emoji.blush
        case _ if ttfl_score < 50:
            return Emoji.smile
        case _ if ttfl_score < 60:
            return Emoji.sunglasses
        case _ if ttfl_score < 80:
            return Emoji.heart_eyes
        case _:
            return Emoji.exploding_head


head = (
    h("meta", charset="utf-8"),
    h("link", rel="stylesheet",
      href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
      integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm",
      crossorigin="anonymous"
      ),
    h("link", rel="icon", href="https://download.vikidia.org/vikidia/fr/images/7/7a/Basketball.png")
)
