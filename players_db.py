import sqlite3

from save_players_to_db import PlayerInfo

connection = sqlite3.connect("players.db")


def get_players_from_db() -> list[PlayerInfo]:
    cursor = connection.cursor()
    cursor.execute("SELECT p.id, p.name, t.id, t.tricode FROM player p INNER JOIN team t on p.team = t.id")

    return [PlayerInfo(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
