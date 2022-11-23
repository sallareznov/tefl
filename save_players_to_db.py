import asyncio
import sqlite3
from itertools import chain
from typing import Coroutine, Any

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

import basketball_reference_urls
from players import Player
from teams import Team

connection = sqlite3.connect("players.db")


async def all_players_from_teams(teams: list[Team]):
    async with ClientSession() as session:
        tasks: list[Coroutine[Any, Any, list[Player]]] = [roster(team, session) for team in teams]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def roster(team: Team, session: ClientSession) -> list[Player]:
    r = await session.request('GET', url=basketball_reference_urls.team_url(team.value[2]))
    text: str = await r.text()
    soup: BeautifulSoup = BeautifulSoup(text, "html.parser")

    return [extract_player_info(player) for player in soup.select("table#roster > tbody > tr")]


def extract_player_info(player_tag: Tag) -> Player:
    player_name_tag = player_tag.select_one("td[data-stat='player']")
    player_profile_tag = player_name_tag.select_one("a")
    player_name = player_profile_tag.text
    player_profile_uri = player_profile_tag.get("href").split(".")[0]
    return Player(name=player_name, profile_uri=player_profile_uri)


def init_player_table():
    connection.execute(
        """
            CREATE TABLE IF NOT EXISTS player(
                name TEXT PRIMARY KEY,
                profile_uri TEXT
            )
        """
    )


def insert_players_into_table(players: list[Player]):
    records = [(player.name, player.profile_uri) for player in players]
    connection.executemany("INSERT INTO player(name, profile_uri) VALUES (?, ?)", records)


def save_players(players: list[Player]):
    init_player_table()
    insert_players_into_table(players)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    all_teams: list[Team] = list(Team)
    all_players: list[Player] = list(chain(*asyncio.run(all_players_from_teams(all_teams))))
    save_players(all_players)
