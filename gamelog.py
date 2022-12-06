from datetime import datetime

from nba_api.stats.endpoints import PlayerGameLog
from unidecode import unidecode

from games import Gamelog, GameLocation, GamelogEntry, GameRealStats
from save_players_to_db import PlayerInfo
from teams import Team


def matching_players(search: str, players: list[PlayerInfo]) -> list[PlayerInfo]:
    """
    Find players whose name matches the search

    :param players: the players to filter in
    :param search: the term to search for
    :return: the list of players whose full name contains the search
    """
    return [player for player in players if matches(search, player.name)]


def matches(search: str, player_name: str) -> bool:
    normalized_search = unidecode(search).lower().replace(".", "").replace("'", "").replace(" ", "")
    normalized_player_name = unidecode(player_name).lower().replace(".", "").replace("'", "").replace(" ", "")
    return normalized_search in normalized_player_name


def compute_gamelog(player: PlayerInfo) -> Gamelog:
    gamelog = PlayerGameLog(player.id).get_dict()["resultSets"][0]["rowSet"]
    gamelog_entries = [gamelog_entry(player, game) for game in gamelog]
    return Gamelog(entries=gamelog_entries)


def extract_matchup_info(matchup: str) -> tuple[GameLocation, Team]:
    _, location_str, opponent_tricode = matchup.split(" ")
    location = GameLocation.from_str(location_str)
    opponent_team = Team.with_nba_tricode(opponent_tricode)
    return location, opponent_team


def gamelog_entry(player: PlayerInfo, game: dict) -> GamelogEntry:
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
