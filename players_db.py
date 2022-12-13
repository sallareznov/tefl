import sqlite3

from players import Player2

connection = sqlite3.connect("players.db", check_same_thread=False)


def get_players_from_db() -> list[Player2]:
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, team FROM player")

    return [Player2(row[0], row[1], row[2]) for row in cursor.fetchall()]


def get_player_by_id(player_id: str) -> Player2:
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, name, team FROM player WHERE id={player_id}")

    (player_id, player_name, team) = cursor.fetchone()

    return Player2(
        id=player_id,
        name=player_name,
        team_tricode=team
    )
