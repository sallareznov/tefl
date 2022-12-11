import json
from datetime import datetime

import requests

from games import Gamelog, GameLocation, GamelogEntry, GameRealStats
from players import Player
from teams import Team


def compute_gamelog(player: Player) -> Gamelog:
    gamelog_url = f"https://stats.nba.com/stats/playergamelog?DateFrom=&DateTo=&LeagueID=&PlayerID={player.id}&Season=2022-23&SeasonType=Regular+Season"
    headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://stats.nba.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    resp = json.loads(requests.get(gamelog_url, headers=headers).text)
    gamelog = resp["resultSets"][0]["rowSet"]
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
