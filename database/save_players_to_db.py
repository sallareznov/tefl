import sqlite3
import time
from sqlite3 import Connection

import requests
from bs4 import BeautifulSoup

from data.player import Player
from database.player_repository import PlayerRepository


def save_players(connection: Connection, repository: PlayerRepository, players: list[Player]):
    repository.init_player_table()
    repository.insert_players(players)
    connection.commit()
    connection.close()


def extract_player(player: dict, illustrations: dict) -> Player:
    name = f"{player['first_name']} {player['last_name']}"
    illustration = illustrations.get(name, "UNKNOWN")

    return Player(
        id=player["id"],
        name=name,
        team_abbreviation=player["team"]["abbreviation"],
        illustration=illustration
    )


def illustrations() -> dict:
    response = requests.get("https://www.statmuse.com/nba/players")
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.select("lazy-img")
    return {image.get("alt"): image.get("src") for image in images}


def all_players_from_bdl_api(illustrations: dict) -> list[Player]:
    url = "https://balldontlie.io/api/v1/players"
    response = requests.get(url).json()

    data = [extract_player(player, illustrations) for player in response["data"] if is_active(player)]
    print(f"page 1: {[p.name for p in data]}")

    next_page = response["meta"]["next_page"]
    total_pages = response["meta"]["total_pages"]

    for page in range(next_page, total_pages + 1):
        time.sleep(1)
        response = requests.get(url, params={"page": page}).json()

        new_data = [extract_player(player, illustrations) for player in response["data"] if is_active(player)]
        print(f"page {page}: {[p.name for p in new_data]}")

        data.extend(new_data)

    return data


def is_active(player: dict) -> bool:
    time.sleep(1)
    stats_url = "https://balldontlie.io/api/v1/stats"
    response = requests.get(stats_url, params={"player_ids[]": player["id"], "seasons[]": "2022"}).json()
    return response["data"] != []


def bdl_api_player_full_name(player: dict) -> str:
    return f"{player['first_name']} {player['last_name']}".replace(".", "")


if __name__ == '__main__':
    connection = sqlite3.connect("players.db", check_same_thread=False)
    repository = PlayerRepository(connection)
    repository.init_player_table()

    all_illustrations = illustrations()
    players = all_players_from_bdl_api(all_illustrations)

    repository.insert_players(players)
    connection.close()
