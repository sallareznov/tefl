from tinyhtml import h

from data.game_stats import GameStats
from emojis import Emoji


class GameTTFLStats:
    bonus: int
    malus: int
    score: int

    def __init__(self, game_stats: GameStats):
        bonus = game_stats.points + game_stats.rebounds + game_stats.assists \
                + game_stats.steals + game_stats.blocks \
                + game_stats.field_goals_made + game_stats.three_pointers_made + game_stats.free_throws_made

        field_goals_missed = game_stats.field_goals_attempted - game_stats.field_goals_made
        three_pointers_missed = game_stats.three_pointers_attempted - game_stats.three_pointers_made
        free_throws_missed = game_stats.free_throws_attempted - game_stats.free_throws_made
        malus = field_goals_missed + three_pointers_missed + free_throws_missed + game_stats.turnovers

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
