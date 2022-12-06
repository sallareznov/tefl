import sqlite3
from dataclasses import dataclass

from nba_api.stats.endpoints import CommonAllPlayers

connection = sqlite3.connect("players.db")


@dataclass
class PlayerInfo:
    id: int
    name: str
    team_id: str
    team_tricode: str


def all_players():
    all = CommonAllPlayers(is_only_current_season=1).get_dict()["resultSets"][0]["rowSet"]
    return [player_info(player) for player in all]


def player_info(player: dict):
    return PlayerInfo(
        id=player[0],
        name=player[2],
        team_id=player[8],
        team_tricode=player[11]
    )


def init_player_table():
    connection.execute(
        """
            CREATE TABLE IF NOT EXISTS team(
                id INTEGER PRIMARY KEY,
                tricode TEXT NOT NULL
            )
        """
    )
    connection.execute(
        """
            CREATE TABLE IF NOT EXISTS player(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                team TEXT NOT NULL,
                FOREIGN KEY(team) REFERENCES team(id)
            )
        """
    )


def insert_players_into_table(players: list[PlayerInfo]):
    team_records = [(player.team_id, player.team_tricode) for player in players]
    player_records = [(player.id, player.name, player.team_id) for player in players]
    connection.executemany("INSERT OR IGNORE INTO team(id, tricode) VALUES (?, ?)", team_records)
    connection.executemany("INSERT INTO player(id, name, team) VALUES (?, ?, ?)", player_records)


def save_players(players: list[PlayerInfo]):
    init_player_table()
    insert_players_into_table(players)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    all_players = all_players()
    save_players(all_players)
