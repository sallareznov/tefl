from dataclasses import dataclass
from sqlite3 import Connection

from data.player import Player


@dataclass
class PlayerRepository:
    connection: Connection

    def init_player_table(self):
        self.connection.execute(
            """
                CREATE TABLE IF NOT EXISTS player(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    team TEXT NOT NULL
                )
            """
        )

    def insert_players(self, players: list[Player]):
        player_records = [(player.id, player.name, player.team_abbreviation) for player in players]
        self.connection.executemany("INSERT OR IGNORE INTO player(id, name, team) VALUES (?, ?, ?)", player_records)

    def get_players_from_db(self) -> list[Player]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, team FROM player")

        return [Player(row[0], row[1], row[2]) for row in cursor.fetchall()]

    def get_player_by_id(self, player_id: str) -> Player:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id, name, team FROM player WHERE id={player_id}")

        (player_id, player_name, team) = cursor.fetchone()

        return Player(
            id=player_id,
            name=player_name,
            team_abbreviation=team
        )
