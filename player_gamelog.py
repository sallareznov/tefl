import requests
from bs4 import BeautifulSoup, Tag
from unidecode import unidecode

from players import Player, GameResult
from players_db import get_players_from_db


def matching_players(players: list[Player], name: str) -> list[Player]:
    return [player for player in players if unidecode(name) in unidecode(player.name)]


# parallelize
def gamelog(player: Player) -> list[GameResult]:
    url = f"https://www.basketball-reference.com{player.profile_uri}/gamelog/2023"
    print(url)
    response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    print(soup.select("tr[id*='pgl_basic.']").__len__())

    return [game_result(log) for log in soup.select("tr[id*='pgl_basic.']")]


def game_result(log: Tag) -> GameResult:
    date = log.select_one("td[data-stat='date_game']").text
    opponent = log.select_one("td[data-stat='opp_id']").text
    (bonus, malus) = ttfl_bonus_malus(log)

    return GameResult(date, opponent, bonus, malus)


def ttfl_bonus_malus(log: Tag) -> (int, int):
    points = select_metric(log, "pts")
    rebounds = select_metric(log, "trb")
    assists = select_metric(log, "ast")
    steals = select_metric(log, "stl")
    blocks = select_metric(log, "blk")
    field_goals_made = select_metric(log, "fg")
    field_goals_attempted = select_metric(log, "fga")
    field_goals_missed = int(field_goals_attempted - field_goals_made)
    three_pointers_made = select_metric(log, "fg3")
    three_pointers_attempted = select_metric(log, "fg3a")
    three_pointers_missed = int(three_pointers_attempted - three_pointers_made)
    free_throws_made = select_metric(log, "ft")
    free_throws_attempted = select_metric(log, "fta")
    free_throws_missed = int(free_throws_attempted - free_throws_made)
    turnovers = select_metric(log, "tov")

    bonus = points + rebounds + assists + steals + blocks + field_goals_made + three_pointers_made + free_throws_made
    malus = field_goals_missed + three_pointers_missed + free_throws_missed + turnovers

    return bonus, malus


def select_metric(log: Tag, data_stat: str) -> int:
    return int(log.select_one(f"td[data-stat='{data_stat}']").text)


if __name__ == '__main__':
    all_players = get_players_from_db()
    print(matching_players(all_players, "Bogdanovic"))
