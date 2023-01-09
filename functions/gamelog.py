from datetime import datetime

import requests

from data.game_location import GameLocation
from data.game_stats import GameStats
from data.player_game import PlayerGame
from data.player_gamelog import PlayerGamelog
from data.team import team_with_bdl_id
from database.player_repository import PlayerRepository


def player_gamelog(player_id: str, repository: PlayerRepository) -> PlayerGamelog:
    player = repository.get_player_by_id(player_id)
    stats_url = "https://balldontlie.io/api/v1/stats"
    response = requests.get(stats_url, params={"seasons[]": "2022", "player_ids[]": player_id}).json()

    entries = [gamelog_entry(game) for game in response["data"] if int(game["min"]) != 0]

    next_page = response["meta"]["next_page"]
    total_pages = response["meta"]["total_pages"]

    for page in range(next_page, total_pages + 1):
        response = requests.get(
            stats_url,
            params={"page": page, "seasons[]": "2022", "player_ids[]": player_id}
        ).json()

        entries.extend([gamelog_entry(game) for game in response["data"] if int(game["min"]) != 0])

    return PlayerGamelog(
        player=player.name,
        team=player.team(),
        games=entries
    )


def gamelog_entry(game: dict) -> PlayerGame:
    date = datetime.strptime(game["game"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    minutes_played = int(game["min"])

    player_team_id = game["player"]["team_id"]

    location, opponent_bdl_id = \
        (GameLocation.HOME, game["game"]["visitor_team_id"]) \
            if game["game"]["home_team_id"] == player_team_id \
            else (GameLocation.AWAY, game["game"]["home_team_id"])

    opponent = team_with_bdl_id(opponent_bdl_id)

    stats = GameStats(
        minutes=int(game["min"]),
        points=game["pts"],
        rebounds=game["reb"],
        assists=game["ast"],
        steals=game["stl"],
        blocks=game["blk"],
        field_goals_made=game["fgm"],
        field_goals_attempted=game["fga"],
        three_pointers_made=game["fg3m"],
        three_pointers_attempted=game["fg3a"],
        free_throws_made=game["ftm"],
        free_throws_attempted=game["fta"],
        turnovers=game["turnover"]
    )

    return PlayerGame(
        date=date,
        opponent=opponent,
        location=location,
        minutes_played=minutes_played,
        stats=stats
    )
