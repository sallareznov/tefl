import time
from datetime import datetime

from nba_api.stats.endpoints import PlayerGameLog

from games import Gamelog, GameLocation, GamelogEntry, GameRealStats
from players import Player
from teams import Team


def compute_gamelog(player: Player) -> Gamelog:
    gamelog = PlayerGameLog(player.id).get_dict()["resultSets"][0]["rowSet"]
    return Gamelog(entries=[gamelog_entry(game) for game in gamelog])


def extract_matchup_info(matchup: str) -> tuple[GameLocation, Team]:
    _, location_str, opponent_tricode = matchup.split(" ")
    location = GameLocation.from_str(location_str)
    opponent_team = Team.with_nba_tricode(opponent_tricode)
    return location, opponent_team


def gamelog_entry(game: dict) -> GamelogEntry:
    date = datetime.strptime(game[3], "%b %d, %Y")

    matchup = game[4]
    location, opponent = extract_matchup_info(matchup)
    minutes_played = game[6]

    real_stats = GameRealStats(
        points=game[24],
        rebounds=game[18],
        assists=game[19],
        steals=game[20],
        blocks=game[21],
        field_goals_made=game[7],
        field_goals_attempted=game[8],
        three_pointers_made=game[10],
        three_pointers_attempted=game[11],
        free_throws_made=game[13],
        free_throws_attempted=game[14],
        turnovers=game[22]
    )

    return GamelogEntry(
        date=date,
        opponent=opponent,
        location=location,
        minutes_played=minutes_played,
        real_stats=real_stats
    )
