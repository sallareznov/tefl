import sqlite3

import players
from players import Player

connection = sqlite3.connect("players.db")


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


def insert_players_into_table(players: list[Player]):
    team_records = [(player.team_id, player.team_tricode) for player in players]
    player_records = [(player.id, player.name, player.team_id) for player in players]
    connection.executemany("INSERT OR IGNORE INTO team(id, tricode) VALUES (?, ?)", team_records)
    connection.executemany("INSERT INTO player(id, name, team) VALUES (?, ?, ?)", player_records)


def save_players(players: list[Player]):
    init_player_table()
    insert_players_into_table(players)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    all_players = players.all_players()
    save_players(all_players)
