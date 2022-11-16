import asyncio
from collections.abc import Coroutine
from typing import Any
from urllib.parse import urlparse

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from ttfl import espn_urls
from ttfl.player import Player
from ttfl.teams import Team


async def roster(team: Team, session: ClientSession) -> list[Player]:
    team_roster_url: str = espn_urls.team_roster(team)
    r = await session.request('GET', url=team_roster_url)
    text: str = await r.text()
    soup: BeautifulSoup = BeautifulSoup(text, "html.parser")

    return [extract_player_info(player) for player in soup.select("tr[data-idx]")]


async def all_rosters(teams: list[Team]):
    async with aiohttp.ClientSession() as session:
        tasks: list[Coroutine[Any, Any, list[Player]]] = [roster(team, session) for team in teams]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def extract_player_info(player_tag: Tag) -> Player:
    player_profile_tag: Tag = player_tag.find_next("td").find_next("td").select_one(".AnchorLink")
    player_profile_url: str = player_profile_tag.get("href")
    # URL example: https://www.espn.com/nba/player/_/id/2566769/malcolm-brogdon

    path = urlparse(player_profile_url).path
    player_id = path.split("/")[5]
    player_url_name = path.split("/")[6]
    player_name: str = player_profile_tag.text
    return Player(id=player_id, name=player_name, name_in_url=player_url_name)
