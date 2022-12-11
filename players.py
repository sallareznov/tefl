from dataclasses import dataclass

from nba_api.stats.endpoints import CommonAllPlayers
from unidecode import unidecode


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


def all_players() -> list[Player]:
    all = CommonAllPlayers(is_only_current_season=1).get_dict()["resultSets"][0]["rowSet"]
    return [player_info(player) for player in all]


def player_info(player: dict) -> Player:
    return Player(
        id=player[0],
        name=player[2],
        team_id=player[8],
        team_tricode=player[11]
    )