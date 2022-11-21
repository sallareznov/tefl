from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag
from tinyhtml import h, html, _h

from ttfl import rosters


@dataclass
class Player:
    name: str
    profile_url: str


class GameResult:
    date: str
    opponent: str
    ttfl_bonus: int
    ttfl_malus: int
    ttfl_score: int

    def __init__(self, date, opponent, bonus, malus):
        self.date = date
        self.opponent = opponent
        self.ttfl_bonus = bonus
        self.ttfl_malus = malus
        self.ttfl_score = bonus - malus


def html_gamelog(name: str) -> _h:
    assert name.__len__() >= 3

    players = rosters.matching_players(name)

    return html()(
        h("style")("table, th, td { border: 1px solid black; }"),
        h("body")(
            (h("div")(
                h("h2")(player.name),
                h("table")(
                    h("tr")(
                        h("th")("Date"),
                        h("th")("Adversaire"),
                        h("th")("Bonus TTFL"),
                        h("th")("Malus TTFL"),
                        h("th")("Score TTFL")
                    ),
                    (h("tr")(
                        h("td")(result.date),
                        h("td")(result.opponent),
                        h("td")(result.ttfl_bonus),
                        h("td")(result.ttfl_malus),
                        h("td")(result.ttfl_score)
                    ) for result in gamelog(player))
                )
            ) for player in players)
        )
    )


def gamelog(player: Player) -> list[GameResult]:
    response = requests.get(f"https://www.basketball-reference.com{player.profile_url}/gamelog/2023")
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

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
    print(html_gamelog("Davis"))
