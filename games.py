from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from statistics import mean

from tinyhtml import h

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

    def html(self):
        return h("span", style="font-weight:bold;")(self.score), self.to_emoji().html()

    def to_emoji(self) -> Emoji:
        if self.score < 10:
            return Emoji.face_vomiting
        if self.score < 20:
            return Emoji.expressionless
        if self.score < 30:
            return Emoji.face_with_rolling_eyes
        if self.score < 35:
            return Emoji.unamused
        if self.score < 40:
            return Emoji.sweat_smile
        if self.score < 45:
            return Emoji.blush
        if self.score < 50:
            return Emoji.smile
        if self.score < 60:
            return Emoji.sunglasses
        if self.score < 80:
            return Emoji.heart_eyes
        else:
            return Emoji.exploding_head


class GameLocation(Enum):
    HOME = "vs.", Emoji.house
    AWAY = "@", Emoji.airplane

    def label(self) -> str: return self.value[0]

    def emoji(self) -> Emoji: return self.value[1]

    @staticmethod
    def from_str(location_str: str): return [loc for loc in list(GameLocation) if loc.label() == location_str][0]

    def html_with_emoji(self): return self.emoji().html()

    def html_with_text(self): return self.label()


class GamelogEntry:
    date: datetime
    opponent: Team
    location: GameLocation
    minutes_played: int
    real_stats: GameRealStats
    ttfl_stats: GameTTFLStats

    def __init__(
            self,
            date: datetime,
            opponent: Team,
            location: GameLocation,
            minutes_played: int,
            real_stats: GameRealStats
    ):
        self.date = date
        self.opponent = opponent
        self.location = location
        self.minutes_played = minutes_played
        self.real_stats = real_stats
        self.ttfl_stats = game_ttfl_stats(real_stats)

    def minutes_played_html(self):
        return self.minutes_played, " ", Emoji.stopwatch.html()


class Gamelog:
    player: str
    team: Team
    entries: list[GamelogEntry]
    games_played: int
    ttfl_average: float

    def __init__(self, player: str, team: Team, entries: list[GamelogEntry]):
        self.player = player
        self.team = team
        self.entries = sorted(entries, key=lambda entry: entry.date, reverse=True)
        self.games_played = entries.__len__()
        ttfl_scores = [entry.ttfl_stats.score for entry in entries]
        self.ttfl_average = 0 if not ttfl_scores else round(mean(ttfl_scores), 1)


def game_ttfl_stats(real_stats: GameRealStats) -> GameTTFLStats:
    bonus = real_stats.points + real_stats.rebounds + real_stats.assists + real_stats.steals + real_stats.blocks \
            + real_stats.field_goals_made + real_stats.three_pointers_made + real_stats.free_throws_made
    field_goals_missed = real_stats.field_goals_attempted - real_stats.field_goals_made
    three_pointers_missed = real_stats.three_pointers_attempted - real_stats.three_pointers_made
    free_throws_missed = real_stats.free_throws_attempted - real_stats.free_throws_made
    malus = field_goals_missed + three_pointers_missed + free_throws_missed + real_stats.turnovers

    return GameTTFLStats(bonus=bonus, malus=malus)
