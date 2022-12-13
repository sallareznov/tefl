import sqlite3

from players import Player2

connection = sqlite3.connect("players.db")


def init_player_table():
    connection.execute(
        """
            CREATE TABLE IF NOT EXISTS player(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                team TEXT NOT NULL
            )
        """
    )


def insert_players_into_table(players: list[Player2]):
    player_records = [(player.id, player.name, player.team_tricode) for player in players]
    connection.executemany("INSERT OR IGNORE INTO player(id, name, team) VALUES (?, ?, ?)", player_records)


def save_players(players: list[Player2]):
    init_player_table()
    insert_players_into_table(players)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    file = open('players.txt', 'r')
    lines = file.read().splitlines()

    players = []

    for line in lines:
        player_id, player_name, team = line.split(",")
        players.append(Player2(player_id, player_name, team))

    save_players(players)

