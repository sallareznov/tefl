from dataclasses import dataclass
from datetime import datetime

from data.game_location import GameLocation
from data.team import Team
from data.team_top_scores import TeamTopScores


@dataclass
class TeamGame:
    date: datetime
    opponent: Team
    location: GameLocation
    own_team_top_scores: TeamTopScores
    opponent_team_top_scores: TeamTopScores
    own_team_inactive_players: list[str]
    opponent_team_inactive_players: list[str]
