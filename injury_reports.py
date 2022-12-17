from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

import numpy as np
import pandas as pd
import tabula
from pandas import DataFrame, Series
from tinyhtml import _h, h, raw

import teams
from games import GameLocation
from teams import Team


class TeamInjuryReportStatus(Enum):
    SUBMITTED = "SUBMITTED"
    NOT_YET_SUBMITTED = "NOT YET SUBMITTED"


class PlayerInjuryStatus(Enum):
    OUT = "Out"
    DOUBTFUL = "Doubtful"
    QUESTIONABLE = "Questionable"
    PROBABLE = "Probable"
    AVAILABLE = "Available"

    @staticmethod
    def with_status(status: str): return next(s for s in PlayerInjuryStatus if s.value == status)


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
    return teams.with_nba_abbreviation(away_team_id), teams.with_nba_abbreviation(home_team_id)


def drop_pdf_headers(frame: DataFrame):
    # set first row as header and then drop it from the data
    frame.columns = frame.iloc[0]
    frame = frame.iloc[1:, :]

    return frame


def transform_frame(frame: DataFrame) -> DataFrame:
    frame = frame[frame["Reason"].notnull()]

    frame[["Player Name", "Current Status"]] = frame["Player Name Current Status"].apply(
        lambda player_name_current_status: Series(split_into_player_name_and_current_status(player_name_current_status))
    )

    frame = frame[["Game Date", "Matchup", "Team", "Player Name", "Current Status", "Reason"]]

    return frame


def split_into_player_name_and_current_status(player_name_current_status):
    if pd.isnull(player_name_current_status):
        return player_name_current_status, player_name_current_status
    else:
        last_name, first_name_and_status = str(player_name_current_status).split(",")
        _, first_name, status = first_name_and_status.split(" ")
        return f"{first_name} {last_name}", status


def get_injury_reports(url: str, date: datetime) -> list[TeamInjuryReport]:
    day_after = date + timedelta(days=1)
    tomorrow_str = day_after.strftime("%m/%d/%Y")
    table = tabula.read_pdf(url, stream=True, guess=False, pages="all")

    dropped = [drop_pdf_headers(f) for f in table]

    frames = [transform_frame(f) for f in dropped if "Player Name Current Status" in f]
    entire_injury_report = pd.DataFrame(np.concatenate(frames), columns=frames[0].columns)

    away_team: Team = None
    home_team: Team = None
    current_report: TeamInjuryReport = None
    all_reports: list[TeamInjuryReport] = []

    for _, row in entire_injury_report.iterrows():
        matchup, team, player_name, reason, status = \
            str(row["Matchup"]), str(row["Team"]), str(row["Player Name"]), \
            str(row["Reason"]), str(row["Current Status"])

        team_nickname = team.split(" ")[-1]

        if matchup != "nan": away_team, home_team = competitors(matchup)

        match team:
            case _ if str(row["Game Date"]) == tomorrow_str:
                break
            case _ if away_team.nickname().__contains__(team_nickname):
                match reason:
                    case TeamInjuryReportStatus.NOT_YET_SUBMITTED.value:
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
            case _ if home_team.nickname().__contains__(team_nickname):
                match reason:
                    case TeamInjuryReportStatus.NOT_YET_SUBMITTED.value:
                        all_reports.append(current_report)
                        current_report = init_report(
                            home_team, away_team, GameLocation.HOME, TeamInjuryReportStatus.NOT_YET_SUBMITTED
                        )
                    case _:
                        all_reports.append(current_report)
                        current_report = init_report(
                            home_team, away_team, GameLocation.HOME, TeamInjuryReportStatus.SUBMITTED
                        )
                        current_report.add_player(player_name, status, reason)
            case _ if status != "nan":
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
