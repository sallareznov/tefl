from data.game_stats import GameStats
from data.game_ttfl_stats import GameTTFLStats
from emojis import Emoji


class PlayerGame2:
    ttfl_stats: GameTTFLStats
    minutes_played: int

    def __init__(self, real_stats: GameStats, minutes_played: int):
        self.minutes_played = minutes_played
        self.real_stats = real_stats
        self.ttfl_stats = GameTTFLStats(real_stats)

    def minutes_played_html(self): return self.minutes_played, " ", Emoji.stopwatch.html()
