from enum import Enum

from emojis import Emoji


class GameLocation(Enum):
    HOME = "vs.", Emoji.house
    AWAY = "@", Emoji.airplane

    def label(self) -> str: return self.value[0]

    def emoji(self) -> Emoji: return self.value[1]

    @staticmethod
    def from_str(location_str: str): return [loc for loc in list(GameLocation) if loc.label() == location_str][0]

    def html_with_emoji(self): return self.emoji().html()

    def html_with_label(self): return self.label()
