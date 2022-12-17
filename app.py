from datetime import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from flask import Flask
from pytz import timezone
from tinyhtml import _h, html, h, raw

import caches
import gamelog
import injury_reports
import live_scores
from games import Gamelog
from injury_reports import PlayerInjuryStatus, TeamInjuryReport, TeamInjuryReportStatus
from players_db import get_players_from_db

app = Flask(__name__)

all_players = get_players_from_db()

caches = caches.Caches()
scheduler = BackgroundScheduler()
scheduler.add_job(caches.clear_latest_injury_report, "cron", minute="*/10")
scheduler.add_job(caches.clear_gamelog_cache, "cron", hour="8", minute="0")
scheduler.start()


@app.route("/")
def homepage():
    return html()(
        h("head")(head),
        h("body")(
            h("div", klass="list-group")(
                homepage_entry("/live", "Scores en live", "Scores TTFL en live de la soirée"),
                homepage_entry("/injuries", "Injury report", "Injury report le plus récent des matchs de la soirée"),
                homepage_entry("/players", "Stats joueurs", "Stats TTFL de tous les joueurs qui ont joué cette saison")
            )
        )
    ).render()


def homepage_entry(route: str, title: str, description: str) -> _h:
    return h("a", href=route, klass="list-group-item list-group-item-action flex-column align-items-start")(
        h("div", klass="d-flex w-100 justify-content-between")(
            h("h5", klass="mb-1")(title)
        ),
        h("p", klass="mb-1")(description)
    )


@app.route("/players")
def list_all_players():
    return html()(
        h("head")(head),
        h("body")(
            h("input", type="text", id="myInput", onkeyup="filterPlayersByName()", placeholder="Nom du joueur...",
              title="Type in a name"),
            h("ul", id="myUL", klass="list-group")(
                h("li", klass="list-group-item")(
                    player.team().logo_html(),
                    " ",
                    h("a", href=f"/gamelog/{player.id}")(player.name)
                ) for player in all_players
            ),
            h("script")(filter_players_by_name_script())
        )
    ).render()


# TODO surnames (AD, KD...)
def filter_players_by_name_script() -> raw:
    return raw(
        """
            function filterPlayersByName() {
                var input, filter, ul, li, a, i, txtValue;
                input = document.getElementById("myInput");
                filter = input.value.toUpperCase();
                ul = document.getElementById("myUL");
                li = ul.getElementsByTagName("li");
                for (i = 0; i < li.length; i++) {
                    a = li[i].getElementsByTagName("a")[0];
                    txtValue = a.textContent || a.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        li[i].style.display = "";
                    } else {
                        li[i].style.display = "none";
                    }
                }
            }
        """
    )


@app.route("/gamelog/<player_id>")
def gamelog_for_player(player_id: str):
    gl = caches.get_gamelog_of_player(player_id) or gamelog.compute_gamelog(player_id)
    caches.add_to_gamelog_cache(player_id, gl)

    return html()(
        h("head")(head),
        h("body")(single_player_gamelog(gl))
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
                            h("th", scope="col", klass="text-center")("Fautes (Tech.)"),
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
                            h("td", klass="text-center")(player_score.status.html()),
                            h("td", klass="text-center")(player_score.fouls_html()),
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
    injury_report = caches.get_latest_injury_report() or injury_reports.get_injury_reports(url, today)
    caches.set_latest_injury_report(injury_report)

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
                        team_injury_report(index, report) for index, report in enumerate(caches.latest_injury_report)
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
                h("td", klass="text-center")(report.matchup_html()),
                report.html_cell_for_injury_status(PlayerInjuryStatus.PROBABLE),
                report.html_cell_for_injury_status(PlayerInjuryStatus.QUESTIONABLE),
                report.html_cell_for_injury_status(PlayerInjuryStatus.DOUBTFUL),
                report.html_cell_for_injury_status(PlayerInjuryStatus.OUT)
            )
        case TeamInjuryReportStatus.NOT_YET_SUBMITTED:
            return h("tr", bgcolor="#C0C0C0")(
                h("th", scope="row")(index + 1),
                h("td")(report.team.html_with_full_name()),
                h("td", klass="text-center")(report.matchup_html()),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ")
            )


def html_cell_for_injury_status(report: TeamInjuryReport, status: PlayerInjuryStatus):
    return h("td", klass="text-center")(
        raw(f"{player.name}<br>") for player in report.players_with_status(status)
    )


def latest_injury_report_url() -> str:
    response = requests.get("https://official.nba.com/nba-injury-report-2022-23-season/")
    soup = BeautifulSoup(response.text, "html.parser")
    injury_reports = soup.select("div[class~=post-injury] a")

    return [report.get("href") for report in injury_reports][-1]


def single_player_gamelog(gamelog: Gamelog):
    return h("div")(
        h("h2")(gamelog.team.logo_html(), " ", gamelog.player, " ", f"[moyenne TTFL: {gamelog.ttfl_average}]"),
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
                ) for (index, result) in enumerate(gamelog.entries)
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
