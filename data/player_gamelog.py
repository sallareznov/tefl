from statistics import mean

from data.player_game import PlayerGame
from data.team import Team


class PlayerGamelog:
    player: str
    team: Team
    games: list[PlayerGame]
    games_played: int
    ttfl_average: float
    is_premium: bool

    def __init__(self, player: str, team: Team, games: list[PlayerGame]):
        self.player = player
        self.team = team
        self.games = sorted(games, key=lambda game: game.date, reverse=True)
        self.games_played = games.__len__()
        ttfl_scores = [game.ttfl_stats.score for game in games]
        self.ttfl_average = 0 if not ttfl_scores else round(mean(ttfl_scores), 1)
        self.is_premium = self.ttfl_average >= 35
