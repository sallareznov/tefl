from datetime import datetime

import requests
from nba_api.stats.endpoints import PlayerGameLog

import players_db
from games import Gamelog, GameLocation, GamelogEntry, GameRealStats
from players import Player
from teams import Team


def compute_bis(player_id: str):
    player = players_db.get_player_by_id(player_id)
    stats_url = "https://balldontlie.io/api/v1/stats"
    response = requests.get(stats_url, params={"seasons[]": "2022", "player_ids[]": {player_id}}).json()

    entries = [gamelog_entry_bis(game) for game in response["data"] if int(game["min"]) != 0]

    next_page = response["meta"]["next_page"]
    total_pages = response["meta"]["total_pages"]

    for page in range(next_page, total_pages + 1):
        response = requests.get(stats_url, params={"page": page, "seasons[]": "2022", "player_ids[]": {player_id}}).json()
        entries.extend([gamelog_entry_bis(game) for game in response["data"] if int(game["min"]) != 0])

    return Gamelog(
        player=player.name,
        team=player.team(),
        entries=entries
    )


def compute_gamelog(player: Player) -> Gamelog:
    gamelog = PlayerGameLog(player_id=player.id, timeout=120).get_dict()["resultSets"][0]["rowSet"]
    return Gamelog(entries=[gamelog_entry(game) for game in gamelog])


def extract_matchup_info(matchup: str) -> tuple[GameLocation, Team]:
    _, location_str, opponent_tricode = matchup.split(" ")
    location = GameLocation.from_str(location_str)
    opponent_team = Team.with_nba_abbreviation(opponent_tricode)
    return location, opponent_team


def gamelog_entry_bis(game: dict):
    date = datetime.strptime(game["game"]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    minutes_played = int(game["min"])

    player_team_id = game["player"]["team_id"]

    location, opponent_bdl_id = \
        (GameLocation.HOME, game["game"]["visitor_team_id"]) if game["game"]["home_team_id"] == player_team_id \
            else (GameLocation.AWAY, game["game"]["home_team_id"])

    opponent = Team.with_bdl_id(opponent_bdl_id)

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
