import time
from dataclasses import dataclass

import requests
from unidecode import unidecode

from teams import Team


@dataclass(eq=False)
class Player2:
    id: int
    name: str
    team_tricode: str

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, another):
        return self.name == another.name

    def team(self) -> Team:
        return Team.with_nba_abbreviation(self.team_tricode)


@dataclass
class Player:
    id: int
    name: str
    team_id: str
    team_tricode: str

    def matches(self, search: str) -> bool:
        normalized_search = unidecode(search).lower().replace(".", "").replace("'", "").replace(" ", "")
        normalized_player_name = unidecode(self.name).lower().replace(".", "").replace("'", "").replace(" ", "")
        return normalized_search in normalized_player_name


def matching_players(search: str, players: list[Player]) -> list[Player]:
    return [player for player in players if player.matches(search)]


def get_players_from_bdl_api() -> list[Player2]:
    print("--> page 1")
    url = "https://balldontlie.io/api/v1/players"
    response = requests.get(url, params={"page": "1"}).json()
    players = [get_player_from_bdl_api(player) for player in response["data"] if is_playing_this_season(player)]

    next_page = response["meta"]["next_page"]
    total_pages = response["meta"]["total_pages"]

    for page in range(next_page, total_pages + 1):
        print(f"--> page {page}")
        response = requests.get(url, params={"page": page}).json()
        players.extend(
            [get_player_from_bdl_api(player) for player in response["data"] if is_playing_this_season(player)])

    return players


def is_playing_this_season(player: dict) -> bool:
    time.sleep(1)
    response = requests.get("https://balldontlie.io/api/v1/stats", {"seasons[]": "2022", "player_ids[]": player["id"]})
    data = response.json()["data"]
    return bool(data)


def get_player_from_bdl_api(player: dict):
    id = player["id"]
    first_name = player["first_name"]
    last_name = player["last_name"]
    full_name = f"{first_name} {last_name}"
    team_code = player["team"]["abbreviation"]

    return Player2(
        id=id,
        name=full_name,
        team_tricode=team_code
    )
