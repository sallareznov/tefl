from dataclasses import dataclass
from statistics import mean

import requests
from bs4 import Tag, BeautifulSoup

import basketball_reference_urls
from players import Player


@dataclass
class GameRealStats:
    points: int
    rebounds: int
    assists: int
    steals: int
    blocks: int
    field_goals_made: int
    field_goals_attempted: int
    three_pointers_made: int
    three_pointers_attempted: int
    free_throws_made: int
    free_throws_attempted: int
    turnovers: int


class GameTTFLStats:
    bonus: int
    malus: int
    score: int

    def __init__(self, bonus: int, malus: int):
        self.bonus = bonus
        self.malus = malus
        self.score = bonus - malus


@dataclass
class GamelogEntry:
    date: str
    opponent: str
    real_stats: GameRealStats
    ttfl_stats: GameTTFLStats


class Gamelog:
    entries: list[GamelogEntry]
    games_played: int
    ttfl_average: float

    def __init__(self, entries: list[GamelogEntry]):
        self.entries = entries
        self.games_played = entries.__len__()
        ttfl_scores = [entry.ttfl_stats.score for entry in entries]
        self.ttfl_average = round(mean(ttfl_scores), 1)


def gamelog(player: Player) -> Gamelog:
    response = requests.get(basketball_reference_urls.player_gamelog_url(player.profile_uri))
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    gamelog_entries = [gamelog_entry(log) for log in soup.select("tr[id*='pgl_basic.']")]

    return Gamelog(entries=gamelog_entries)


def gamelog_entry(log: Tag) -> GamelogEntry:
    date = log.select_one("td[data-stat='date_game']").text
    opponent = log.select_one("td[data-stat='opp_id']").text
    real_stats = game_real_stats(log)
    ttfl_stats = game_ttfl_stats(real_stats)

    return GamelogEntry(date=date, opponent=opponent, real_stats=real_stats, ttfl_stats=ttfl_stats)


def game_real_stats(log: Tag) -> GameRealStats:
    return GameRealStats(
        points=select_metric(log, "pts"),
        rebounds=select_metric(log, "trb"),
        assists=select_metric(log, "ast"),
        steals=select_metric(log, "stl"),
        blocks=select_metric(log, "blk"),
        field_goals_made=select_metric(log, "fg"),
        field_goals_attempted=select_metric(log, "fga"),
        three_pointers_made=select_metric(log, "fg3"),
        three_pointers_attempted=select_metric(log, "fg3a"),
        free_throws_made=select_metric(log, "ft"),
        free_throws_attempted=select_metric(log, "fta"),
        turnovers=select_metric(log, "tov")
    )


def game_ttfl_stats(real_stats: GameRealStats) -> GameTTFLStats:
    bonus = real_stats.points + real_stats.rebounds + real_stats.assists + real_stats.steals + real_stats.blocks \
            + real_stats.field_goals_made + real_stats.three_pointers_made + real_stats.free_throws_made
    field_goals_missed = real_stats.field_goals_attempted - real_stats.field_goals_made
    three_pointers_missed = real_stats.three_pointers_attempted - real_stats.three_pointers_made
    free_throws_missed = real_stats.free_throws_attempted - real_stats.free_throws_made
    malus = field_goals_missed + three_pointers_missed + free_throws_missed + real_stats.turnovers

    return GameTTFLStats(bonus=bonus, malus=malus)


def select_metric(log: Tag, data_stat: str) -> int:
    return int(log.select_one(f"td[data-stat='{data_stat}']").text)
