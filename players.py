from dataclasses import dataclass


@dataclass
class Player:
    name: str
    profile_uri: str


class GameResult:
    date: str
    opponent: str
    ttfl_bonus: int
    ttfl_malus: int
    ttfl_score: int

    def __init__(self, date, opponent, bonus, malus):
        self.date = date
        self.opponent = opponent
        self.ttfl_bonus = bonus
        self.ttfl_malus = malus
        self.ttfl_score = bonus - malus
