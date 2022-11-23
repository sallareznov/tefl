import sqlite3

from players import Player

connection = sqlite3.connect("players.db")


def get_players_from_db() -> list[Player]:
    cursor = connection.cursor()
    cursor.execute("SELECT name, profile_uri FROM player")

    return [Player(row[0], row[1]) for row in cursor.fetchall()]
