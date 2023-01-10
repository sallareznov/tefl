from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pytz import timezone
from tinyhtml import h, html, raw, _h

from data.caches import Caches
from data.player_injury_status import PlayerInjuryStatus
from data.team_injury_report import TeamInjuryReport
from functions import injury_reports
from pages import common


def injury_report(caches: Caches):
    url = latest_injury_report_url()
    today = datetime.now(timezone("US/Eastern"))
    latest_injury_report = caches.get_latest_injury_report() or injury_reports.get_injury_reports(url, today)
    caches.set_latest_injury_report(latest_injury_report)

    return html()(
        h("head")(common.head),
        h("body")(
            h("div")(
                h("h2")("Injury Report"),
                h("table", klass="table table-responsive table-bordered")(
                    h("thead", klass="table-light")(
                        h("tr")(
                            h("th", klass="text-center", style="background-color: gray;", scope="col")("Équipe"),
                            h("th", klass="text-center", style="background-color: gray;", scope="col")("Adversaire"),
                            injury_status_header("#007500", "PROBABLE", "(80% de chances de jouer)"),
                            injury_status_header("#778A35", "QUESTIONABLE", "(50% de chances de jouer)"),
                            injury_status_header("#A35900", "DOUBTFUL", "(25% de chances de jouer)"),
                            injury_status_header("#8B0903", "OUT", "(0% de chances de jouer)")
                        )
                    ),
                    h("tbody", klass="table-group-divider")(
                        team_injury_report(report) for report in caches.latest_injury_report
                    )
                )
            ),
            common.bootstrap_js_script
        )
    ).render()


def html_cell_for_injury_status(report: TeamInjuryReport, status: PlayerInjuryStatus) -> _h:
    return h("td", klass="text-center")(
        raw(f"{player.name}<br>") for player in report.players_with_status(status)
    )


def latest_injury_report_url() -> str:
    response = requests.get("https://official.nba.com/nba-injury-report-2022-23-season/")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.select("div[class~=post-injury] a")[-1].get("href")


def injury_status_header(bg_color: str, title: str, description: str) -> _h:
    return h("th", klass="text-center", scope="col", style=f"color:white; background-color:{bg_color}")(
        h("span", style="font-weight:bold;")(title), h("br"), h("span")(description),
    )


def team_injury_report(report: injury_reports.TeamInjuryReport) -> _h:
    match report.status:
        case injury_reports.TeamInjuryReportStatus.SUBMITTED:
            return h("tr")(
                h("td")(report.team.html_with_full_name()),
                h("td", klass="text-center")(report.matchup_html()),
                report.html_cell_for_injury_status(PlayerInjuryStatus.PROBABLE),
                report.html_cell_for_injury_status(PlayerInjuryStatus.QUESTIONABLE),
                report.html_cell_for_injury_status(PlayerInjuryStatus.DOUBTFUL),
                report.html_cell_for_injury_status(PlayerInjuryStatus.OUT)
            )
        case injury_reports.TeamInjuryReportStatus.NOT_YET_SUBMITTED:
            return h("tr", bgcolor="#C0C0C0")(
                h("td")(report.team.html_with_full_name()),
                h("td", klass="text-center")(report.matchup_html()),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ"),
                h("td", klass="text-center")("PAS ENCORE PUBLIÉ")
            )
