from datetime import datetime

import pandas
from pandas import DataFrame
from unidecode import unidecode

import basketball_reference_urls
import scores
from games import Gamelog, GameLocation, GamelogEntry
from players import Player
from teams import Team


def matching_players(players: list[Player], search: str) -> list[Player]:
    return [player for player in players if unidecode(search).lower() in unidecode(player.name).lower()]


def compute_gamelog(player: Player) -> Gamelog:
    data_frame = pandas.read_html(
        basketball_reference_urls.player_gamelog_url(player.profile_uri),
        match="2022-23 Regular Season"
    )[0]

    gamelog_entries = [
        gamelog_entry(data_frame, i)
        for i in range(data_frame.index.stop)
        if data_frame["GS"][i] in [0, "0", 1, "1"]
    ]

    print(gamelog_entries.__len__())

    return Gamelog(entries=gamelog_entries)


def gamelog_entry(data_frame: DataFrame, index: int) -> GamelogEntry:
    date_str = data_frame["Date"][index]
    date = datetime.strptime(date_str, '%Y-%m-%d')

    opponent_short_name = data_frame["Opp"][index]
    opponent = Team.with_basketball_reference_id(opponent_short_name)

    game_location_text = data_frame["Unnamed: 5"][index]
    location = GameLocation.AWAY if game_location_text == "@" else GameLocation.HOME

    time_played = data_frame["MP"][index]
    (minutes, seconds) = [int(x) for x in time_played.split(":")]
    minutes_played = minutes if seconds <= 30 else minutes + 1

    real_stats = scores.game_real_stats(data_frame, index)
    ttfl_stats = scores.game_ttfl_stats(real_stats)

    return GamelogEntry(
        date=date,
        opponent=opponent,
        location=location,
        minutes_played=minutes_played,
        real_stats=real_stats,
        ttfl_stats=ttfl_stats
    )






