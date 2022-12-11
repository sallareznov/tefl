import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto

import numpy as np
import pandas as pd
import tabula
from pandas import DataFrame
from tinyhtml import _h, h, raw

from games import GameLocation
from teams import Team


class TeamInjuryReportStatus(Enum):
    SUBMITTED = auto()
    NOT_YET_SUBMITTED = auto()


class PlayerInjuryStatus(Enum):
    OUT = "Out"
    DOUBTFUL = "Doubtful"
    QUESTIONABLE = "Questionable"
    PROBABLE = "Probable"
    AVAILABLE = "Available"

    @staticmethod
    def with_status(status: str):
        return next(s for s in PlayerInjuryStatus if s.value == status)


@dataclass
class InjuredPlayer:
    name: str
    status: PlayerInjuryStatus
    reason: str
    # premium: bool


@dataclass
class TeamInjuryReport:
    team: Team
    opponent: Team
    location: GameLocation
    status: TeamInjuryReportStatus
    injured_players: list[InjuredPlayer]

    def add_player(self, name: str, status: str, reason: str):
        self.injured_players.append(
            InjuredPlayer(
                name=name,
                status=PlayerInjuryStatus.with_status(status),
                reason=reason
            )
        )

    def players_with_status(self, status: PlayerInjuryStatus):
        return [player for player in self.injured_players if player.status == status]

    def html_cell_for_injury_status(self, status: PlayerInjuryStatus) -> _h:
        return h("td", klass="text-center")(
            raw(f"{player.name}<br>") for player in self.players_with_status(status)
        )


def competitors(game: str) -> (Team, Team):
    (away_team_id, home_team_id) = game.split("@")
    return Team.with_nba_tricode(away_team_id), Team.with_nba_tricode(home_team_id)


def transform_frame(frame: DataFrame) -> DataFrame:
    # set first row as header and then drop it from the data
    frame.columns = frame.iloc[0]
    frame = frame.iloc[1:, :]

    name_column = frame["Player Name Current Status"].apply(
        lambda x: extract_name_column(x)
    )

    status_column = frame["Player Name Current Status"].apply(lambda x: str(x).split(" ")[-1])

    frame = frame.join(status_column.to_frame(name="Current Status"))
    frame = frame.join(name_column.to_frame(name="Player Name"))
    frame = frame.drop(["Player Name Current Status"], axis=1)

    frame = frame[["Game Date", "Game Time", "Matchup", "Team", "Player Name", "Current Status", "Reason"]]
    # frame = frame.loc[str(frame["Current Status"]).isdigit() is True]

    return frame


def extract_name_column(x):
    match x:
        case _ if pd.isnull(x) | bool(re.search("Page \d of \d", str(x))):
            return x
        case _:
            last_name, first_name_and_status = str(x).split(",")
            _, first_name, status = first_name_and_status.split(" ")
            return f"{first_name} {last_name}"


def get_injury_reports(url: str, date: datetime) -> list[TeamInjuryReport]:
    day_after = date + timedelta(days=1)
    tomorrow_str = day_after.strftime("%m/%d/%Y")
    table = tabula.read_pdf(url, stream=True, guess=False, pages="all")
    frames = [transform_frame(f) for f in table]
    entire_injury_report = pd.DataFrame(np.concatenate(frames), columns=frames[0].columns)

    away_team: Team = None
    home_team: Team = None
    current_report: TeamInjuryReport = None
    all_reports: list[TeamInjuryReport] = []

    for index, row in entire_injury_report.iterrows():
        matchup, team, player_name, reason, status = \
            str(row["Matchup"]), str(row["Team"]), str(row["Player Name"]), \
            str(row["Reason"]), str(row["Current Status"])

        if matchup not in ["nan", "Matchup"]:
            away_team, home_team = competitors(matchup)

        # TODO improve
        match team:
            case _ if str(row["Game Date"]) == tomorrow_str:
                break
            case _ if away_team.full_name() == team:
                match reason:
                    case "NOT YET SUBMITTED":
                        all_reports.append(current_report)
                        current_report = init_report(
                            away_team, home_team, GameLocation.AWAY, TeamInjuryReportStatus.NOT_YET_SUBMITTED
                        )
                    case _:
                        all_reports.append(current_report)
                        current_report = init_report(
                            away_team, home_team, GameLocation.AWAY, TeamInjuryReportStatus.SUBMITTED
                        )
                        current_report.add_player(player_name, status, reason)
            case _ if home_team.full_name() == team:
                match reason:
                    case "NOT YET SUBMITTED":
                        all_reports.append(current_report)
                        current_report = TeamInjuryReport(
                            team=home_team,
                            opponent=away_team,
                            location=GameLocation.HOME,
                            status=TeamInjuryReportStatus.NOT_YET_SUBMITTED,
                            injured_players=[]
                        )
                    case _:
                        all_reports.append(current_report)
                        current_report = TeamInjuryReport(
                            team=home_team,
                            opponent=away_team,
                            location=GameLocation.HOME,
                            status=TeamInjuryReportStatus.SUBMITTED,
                            injured_players=[]
                        )
                        current_report.add_player(player_name, status, reason)
            case _ if (status not in ["nan", "Current Status"]) and not status.isdigit():
                current_report.add_player(player_name, status, reason)

    all_reports.append(current_report)

    return [report for report in all_reports if report is not None]


def init_report(
        team: Team,
        opponent: Team,
        location: GameLocation,
        status: TeamInjuryReportStatus
) -> TeamInjuryReport:
    return TeamInjuryReport(
        team=team,
        opponent=opponent,
        location=location,
        status=status,
        injured_players=[]
    )
