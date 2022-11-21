import asyncio
from collections.abc import Coroutine
from itertools import chain
from typing import Any

from aiohttp import ClientSession

from ttfl.players import Player
from ttfl.teams import Team


async def all_nba_players(teams: list[Team]):
    async with ClientSession() as session:
        tasks: list[Coroutine[Any, Any, list[Player]]] = [team.roster(session) for team in teams]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def matching_players(name: str) -> list[Player]:
    return [player for player in all_players if name in player.name]


all_teams = list(Team)
all_players: list[Player] = list(chain(*asyncio.run(all_nba_players(all_teams))))

if __name__ == '__main__':
    print(all_teams)
    print(matching_players("Davis"))
