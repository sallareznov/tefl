from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from statistics import mean

import requests
from bs4 import Tag, BeautifulSoup

import basketball_reference_urls
from players import Player
from teams import Team


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


class GameLocation(Enum):
    HOME = "Dom."
    AWAY = "Ext."


@dataclass
class GamelogEntry:
    date: datetime
    opponent: Team
    location: GameLocation
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
        self.ttfl_average = 0 if not ttfl_scores else round(mean(ttfl_scores), 1)


def gamelog(player: Player) -> Gamelog:
    response = requests.get(basketball_reference_urls.player_gamelog_url(player.profile_uri))
    soup = BeautifulSoup(response.text, "html.parser")
    gamelog_entries = [gamelog_entry(log) for log in soup.select("tr[id*='pgl_basic.']")]

    return Gamelog(entries=gamelog_entries)


def gamelog_entry(log: Tag) -> GamelogEntry:
    date_str = select_cell(log, "date_game")
    date = datetime.strptime(date_str, '%Y-%m-%d')
    opponent_short_name = select_cell(log, "opp_id")
    opponent = next(team for team in list(Team) if team.value[2] == opponent_short_name)
    game_location_text = select_cell(log, "game_location")
    location = GameLocation.AWAY if game_location_text == "@" else GameLocation.HOME
    real_stats = game_real_stats(log)
    ttfl_stats = game_ttfl_stats(real_stats)

    return GamelogEntry(
        date=date,
        opponent=opponent,
        location=location,
        real_stats=real_stats,
        ttfl_stats=ttfl_stats
    )


def game_real_stats(log: Tag) -> GameRealStats:
    return GameRealStats(
        points=int(select_cell(log, "pts")),
        rebounds=int(select_cell(log, "trb")),
        assists=int(select_cell(log, "ast")),
        steals=int(select_cell(log, "stl")),
        blocks=int(select_cell(log, "blk")),
        field_goals_made=int(select_cell(log, "fg")),
        field_goals_attempted=int(select_cell(log, "fga")),
        three_pointers_made=int(select_cell(log, "fg3")),
        three_pointers_attempted=int(select_cell(log, "fg3a")),
        free_throws_made=int(select_cell(log, "ft")),
        free_throws_attempted=int(select_cell(log, "fta")),
        turnovers=int(select_cell(log, "tov"))
    )


def game_ttfl_stats(real_stats: GameRealStats) -> GameTTFLStats:
    bonus = real_stats.points + real_stats.rebounds + real_stats.assists + real_stats.steals + real_stats.blocks \
            + real_stats.field_goals_made + real_stats.three_pointers_made + real_stats.free_throws_made
    field_goals_missed = real_stats.field_goals_attempted - real_stats.field_goals_made
    three_pointers_missed = real_stats.three_pointers_attempted - real_stats.three_pointers_made
    free_throws_missed = real_stats.free_throws_attempted - real_stats.free_throws_made
    malus = field_goals_missed + three_pointers_missed + free_throws_missed + real_stats.turnovers

    return GameTTFLStats(bonus=bonus, malus=malus)


def select_cell(log: Tag, data_stat: str) -> str:
    return log.select_one(f"td[data-stat='{data_stat}']").text
