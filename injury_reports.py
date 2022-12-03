from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np
import pandas as pd
import tabula
from pandas import DataFrame
from pytz import timezone

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


@dataclass
class TeamInjuryReport:
    team: Team
    opponent: Team
    location: GameLocation
    state: TeamInjuryReportStatus
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


def competitors(game: str) -> (Team, Team):
    (away_team_id, home_team_id) = game.split("@")
    return Team.with_nba_id(away_team_id), Team.with_nba_id(home_team_id)


def transform_frame(frame: DataFrame) -> DataFrame:
    # set first row as header and then drop it from the data
    frame.columns = frame.iloc[0]
    frame = frame.iloc[1:, :]

    name_column = frame["Player Name Current Status"].apply(
        lambda x: " ".join(str(x).split(" ")[:-1][::-1]).replace(",", "")
    )
    status_column = frame["Player Name Current Status"].apply(lambda x: str(x).split(" ")[-1])

    frame = frame.join(status_column.to_frame(name="Current Status"))
    frame = frame.join(name_column.to_frame(name="Player Name"))
    frame = frame.drop(["Player Name Current Status"], axis=1)
    print(list(np.where(frame["Game Date"].notnull())))
    today = datetime.now(timezone("US/Eastern"))
    today_str = today.strftime("%m/%d/%Y")
    tomorrow = today + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%m/%d/%Y")
    print(today_str)
    print(tomorrow_str)

    frame = frame[["Game Date", "Game Time", "Matchup", "Team", "Player Name", "Current Status", "Reason"]]
    # frame = frame.loc[str(frame["Current Status"]).isdigit() is True]

    return frame


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

        match team:
            case _ if str(row["Game Date"]) == tomorrow_str:
                break
            case _ if team != "nan" and away_team.equals(team) and reason == "NOT YET SUBMITTED":
                all_reports.append(current_report)
                current_report = TeamInjuryReport(
                    team=away_team,
                    opponent=home_team,
                    location=GameLocation.AWAY,
                    state=TeamInjuryReportStatus.NOT_YET_SUBMITTED,
                    injured_players=[]
                )
            case _ if team != "nan" and home_team.equals(team) and reason == "NOT YET SUBMITTED":
                all_reports.append(current_report)
                current_report = TeamInjuryReport(
                    team=home_team,
                    opponent=away_team,
                    location=GameLocation.HOME,
                    state=TeamInjuryReportStatus.NOT_YET_SUBMITTED,
                    injured_players=[]
                )
            case _ if team != "nan" and away_team.equals(team):
                all_reports.append(current_report)
                current_report = TeamInjuryReport(
                    team=away_team,
                    opponent=home_team,
                    location=GameLocation.AWAY,
                    state=TeamInjuryReportStatus.SUBMITTED,
                    injured_players=[]
                )
                current_report.add_player(player_name, status, reason)
            case _ if team != "nan" and home_team.equals(team):
                all_reports.append(current_report)
                current_report = TeamInjuryReport(
                    team=home_team,
                    opponent=away_team,
                    location=GameLocation.HOME,
                    state=TeamInjuryReportStatus.SUBMITTED,
                    injured_players=[]
                )
                current_report.add_player(player_name, status, reason)
            case _ if (status not in ["nan", "Current Status"]) and not status.isdigit():
                current_report.add_player(player_name, status, reason)

    all_reports.append(current_report)

    return [report for report in all_reports if report is not None]
