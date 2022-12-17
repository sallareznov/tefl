from dataclasses import dataclass

import teams
from teams import Team


@dataclass(eq=False)
class Player:
    id: int
    name: str
    team_tricode: str

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, another) -> bool:
        return self.name == another.name

    def team(self) -> Team:
        return teams.with_nba_abbreviation(self.team_tricode)
