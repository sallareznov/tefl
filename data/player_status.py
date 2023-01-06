from enum import Enum

from tinyhtml import raw

from emojis import Emoji


class PlayerStatus(Enum):
    ON_COURT = Emoji.stadium
    ON_BENCH = Emoji.chair
    OUT = Emoji.not_permitted

    @staticmethod
    def of_player(player: dict):
        if "notPlayingReason" in player:
            return PlayerStatus.OUT
        elif player["oncourt"] == "1":
            return PlayerStatus.ON_COURT
        else:
            return PlayerStatus.ON_BENCH

    def html(self) -> raw:
        return self.value.html()
