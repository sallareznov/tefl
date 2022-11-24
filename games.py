from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from statistics import mean

import pandas

from teams import Team


@dataclass
class GameRealStats:
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int
    field_goals_made: int
    field_goals_attempted: int
    three_pointers_made: int
    three_pointers_attempted: int
    free_throws_made: int
    free_throws_attempted: int
    turnovers: int


class GameTTFLStats:
    bonus: int
    malus: int
    score: int

    def __init__(self, bonus: int, malus: int):
        self.bonus = bonus
        self.malus = malus
        self.score = bonus - malus


class GameLocation(Enum):
    HOME = "Dom."
    AWAY = "Ext."


@dataclass
class GamelogEntry:
    date: datetime
    opponent: Team
    location: GameLocation
    minutes_played: int
    real_stats: GameRealStats
    ttfl_stats: GameTTFLStats


class Gamelog:
    entries: list[GamelogEntry]
    games_played: int
    ttfl_average: float

    def __init__(self, entries: list[GamelogEntry]):
        self.entries = entries
        self.games_played = entries.__len__()
        ttfl_scores = [entry.ttfl_stats.score for entry in entries]
        self.ttfl_average = 0 if not ttfl_scores else round(mean(ttfl_scores), 1)


if __name__ == '__main__':
    table_ESPN = pandas.read_html(
        "https://www.espn.co.uk/nba/boxscore/_/gameId/401468415"
    )

    # print(table_MN[0][["PTS", "TRB", "AST", "STL", "BLK", "FG", "FGA", "3P", "3PA", "FT", "FTA", "TOV"]])

    # print(table_ESPN[0][["PTS", "REB", "AST", "STL", "BLK", "FG", "3PT", "FT", "TO"]])
    # print(table_ESPN[2][[1, 2, 3]])
    # print(table_ESPN[1])
    # print([x.columns for x in table_ESPN])
