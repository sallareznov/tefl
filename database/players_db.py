import sqlite3

from data.player import Player

connection = sqlite3.connect("database/players.db", check_same_thread=False)


def get_players_from_db() -> list[Player]:
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, team FROM player")

    return [Player(row[0], row[1], row[2]) for row in cursor.fetchall()]


def get_player_by_id(player_id: str) -> Player:
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, name, team FROM player WHERE id={player_id}")

    (player_id, player_name, team) = cursor.fetchone()

    return Player(
        id=player_id,
        name=player_name,
        team_tricode=team
    )
