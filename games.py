from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from statistics import mean

from tinyhtml import frag

from emojis import Emoji
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
    HOME = "Dom.", Emoji.house
    AWAY = "Ext.", Emoji.airplane

    def html(self):
        return frag(self.value[0], self.value[1].html())


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
        self.entries = sorted(entries, key=lambda entry: entry.date, reverse=True)
        self.games_played = entries.__len__()
        ttfl_scores = [entry.ttfl_stats.score for entry in entries]
        self.ttfl_average = 0 if not ttfl_scores else round(mean(ttfl_scores), 1)
