import dataclasses
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
                    team TEXT NOT NULL,
                    illustration TEXT NOT NULL
                )
            """
        )
        self.connection.commit()

    def insert_players(self, players: list[Player]):
        player_records = [dataclasses.astuple(player) for player in players]
        self.connection.executemany(
            "INSERT OR IGNORE INTO player(id, name, team, illustration) VALUES (?, ?, ?, ?)",
            player_records
        )
        self.connection.commit()

    def get_players_from_db(self) -> list[Player]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, team, illustration FROM player")

        return [Player(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]

    def get_player_by_id(self, player_id: str) -> Player:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id, name, team, illustration FROM player WHERE id={player_id}")

        (player_id, player_name, team, illustration) = cursor.fetchone()

        return Player(
            id=player_id,
            name=player_name,
            team_abbreviation=team,
            illustration=illustration
        )
