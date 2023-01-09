from datetime import datetime

from data.game_location import GameLocation
from data.game_stats import GameStats
from data.game_ttfl_stats import GameTTFLStats
from emojis import Emoji
from data.team import Team


class PlayerGame:
    date: datetime
    opponent: Team
    location: GameLocation
    minutes_played: int
    ttfl_stats: GameTTFLStats

    def __init__(
        self,
        date: datetime,
        opponent: Team,
        location: GameLocation,
        minutes_played: int,
        stats: GameStats
    ):
        self.date = date
        self.opponent = opponent
        self.location = location
        self.minutes_played = minutes_played
        self.ttfl_stats = GameTTFLStats(stats)

    def minutes_played_html(self): return self.minutes_played, " ", Emoji.stopwatch.html()
