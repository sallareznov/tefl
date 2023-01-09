import sqlite3

from data.player import Player
from database.player_repository import PlayerRepository


def save_players(repository: PlayerRepository, players: list[Player]):
    repository.init_player_table()
    repository.insert_players(players)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    file = open('players.txt', 'r')
    lines = file.read().splitlines()

    players = []

    for line in lines:
        player_id, player_name, team = line.split(",")
        players.append(Player(player_id, player_name, team))

    connection = sqlite3.connect("players.db", check_same_thread=False)
    repository = PlayerRepository(connection)
    save_players(repository, players)
