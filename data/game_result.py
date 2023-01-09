from enum import Enum

from tinyhtml import h


class GameResult(Enum):
    WIN = "W"
    LOSS = "L"

    def html(self): return h("span", style="color:red;")(self.value)
