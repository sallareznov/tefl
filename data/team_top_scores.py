from dataclasses import dataclass

from tinyhtml import _h, h

from data.player_ttfl_score import PlayerTTFLScore
from emojis import Emoji


@dataclass
class TeamTopScores:
    leader: PlayerTTFLScore
    second_best: PlayerTTFLScore
    third_best: PlayerTTFLScore

    def html(self) -> _h:
        return h("ul")(
            h("li")(TeamTopScores.player_score_info(self.leader, Emoji.gold_medal)),
            h("li")(TeamTopScores.player_score_info(self.second_best, Emoji.silver_medal)),
            h("li")(TeamTopScores.player_score_info(self.third_best, Emoji.bronze_medal))
        )

    @staticmethod
    def player_score_info(player_score_info: PlayerTTFLScore, emoji: Emoji):
        return emoji.html(), \
               " ", \
               f"{player_score_info.name} ({player_score_info.position}): {player_score_info.ttfl_score}"
