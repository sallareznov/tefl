from dataclasses import dataclass

from data.team import Team, team_with_nba_abbreviation


@dataclass(eq=False)
class Player:
    id: int
    name: str
    team_abbreviation: str

    def __hash__(self) -> int: return hash(self.name)

    def __eq__(self, another) -> bool: return self.name == another.name

    def team(self) -> Team: return team_with_nba_abbreviation(self.team_abbreviation)
