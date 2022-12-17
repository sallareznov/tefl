from datetime import datetime

import requests

import players_db
import teams
from games import Gamelog, GameLocation, GamelogEntry, GameRealStats


def compute_gamelog(player_id: str):
    player = players_db.get_player_by_id(player_id)
    stats_url = "https://balldontlie.io/api/v1/stats"
    response = requests.get(stats_url, params={"seasons[]": "2022", "player_ids[]": {player_id}}).json()

    entries = [gamelog_entry(game) for game in response["data"] if int(game["min"]) != 0]

    next_page = response["meta"]["next_page"]
    total_pages = response["meta"]["total_pages"]

    for page in range(next_page, total_pages + 1):
        response = requests.get(
            stats_url,
            params={"page": page, "seasons[]": "2022", "player_ids[]": {player_id}}
        ).json()
        entries.extend([gamelog_entry(game) for game in response["data"] if int(game["min"]) != 0])

    return Gamelog(
        player=player.name,
        team=player.team(),
        entries=entries
    )


def gamelog_entry(game: dict):
    date = datetime.strptime(game["game"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    minutes_played = int(game["min"])

    player_team_id = game["player"]["team_id"]

    location, opponent_bdl_id = \
        (GameLocation.HOME, game["game"]["visitor_team_id"]) if game["game"]["home_team_id"] == player_team_id \
            else (GameLocation.AWAY, game["game"]["home_team_id"])

    opponent = teams.with_bdl_id(opponent_bdl_id)

    real_stats = GameRealStats(
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

    return GamelogEntry(
        date=date,
        opponent=opponent,
        location=location,
        minutes_played=minutes_played,
        real_stats=real_stats
    )
