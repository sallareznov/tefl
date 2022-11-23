from dataclasses import dataclass

from unidecode import unidecode


@dataclass
class Player:
    name: str
    profile_uri: str


def matching_players(players: list[Player], search: str) -> list[Player]:
    return [player for player in players if unidecode(search).lower() in unidecode(player.name).lower()]
