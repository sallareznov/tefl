import json

from nba_api.stats.endpoints.playergamelog import PlayerGameLog
from nba_api.stats.static.players import find_players_by_full_name
from numpy import mean
from toolz import pipe


def tefl_total(log: dict[int, int]) -> int:
    points = log[24]
    rebounds = log[18]
    assists = log[19]
    steals = log[20]
    blocks = log[21]
    field_goals_made = log[7]
    field_goals_attempted = log[8]
    three_point_made = log[10]
    three_point_attempted = log[11]
    free_throws_made = log[13]
    free_throws_attempted = log[14]

    field_goals_missed = field_goals_attempted - field_goals_made
    three_point_missed = three_point_attempted - three_point_made
    free_throws_missed = free_throws_attempted - free_throws_made
    turnovers = log[22]

    bonus = points + rebounds + assists + steals + blocks + field_goals_made + three_point_made + free_throws_made
    malus = field_goals_missed + three_point_missed + free_throws_missed + turnovers

    return bonus - malus


def get_player_id(name: str) -> int:
    return find_players_by_full_name(name)[0]["id"]


def get_player_gamelog(player_id: int) -> dict[any]:
    game_log = PlayerGameLog(player_id)
    game_log_json = json.loads(game_log.get_json())
    return game_log_json["resultSets"][0]["rowSet"]


def get_tefl_totals(all_stats: dict[any]) -> list[int]:
    return list(map(tefl_total, all_stats))


def tefl_average(tefl_totals: list[int]) -> float:
    return round(mean(tefl_totals).item(), 1)


def tefl_totals_for_player(name: str) -> list[int]:
    return pipe(name, get_player_id, get_player_gamelog, get_tefl_totals)


def tefl_average_for_player(name: str) -> float:
    return pipe(name, get_player_id, get_player_gamelog, get_tefl_totals, tefl_average)