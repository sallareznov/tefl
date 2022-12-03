from bs4 import Tag
from pandas import DataFrame

from emojis import Emoji
from games import GameRealStats, GameTTFLStats


def get_ttfl_scores(boxscore: Tag):
    lines = boxscore.select("tr[class~=Table__TR]")
    stat_lines = [line for line in lines if line.select("td")[0].text.isdigit()]
    stats = [game_stats(line) for line in stat_lines]
    ttfl_stats = [game_ttfl_stats(s) for s in stats]

    return [s.score for s in ttfl_stats]


def game_real_stats(data_frame: DataFrame, index: int) -> GameRealStats:
    return GameRealStats(
        points=int(data_frame["PTS"][index]),
        rebounds=int(data_frame["TRB"][index]),
        assists=int(data_frame["AST"][index]),
        steals=int(data_frame["STL"][index]),
        blocks=int(data_frame["BLK"][index]),
        field_goals_made=int(data_frame["FG"][index]),
        field_goals_attempted=int(data_frame["FGA"][index]),
        three_pointers_made=int(data_frame["3P"][index]),
        three_pointers_attempted=int(data_frame["3PA"][index]),
        free_throws_made=int(data_frame["FT"][index]),
        free_throws_attempted=int(data_frame["FTA"][index]),
        turnovers=int(data_frame["TOV"][index])
    )


def game_ttfl_stats(real_stats: GameRealStats) -> GameTTFLStats:
    bonus = real_stats.points + real_stats.rebounds + real_stats.assists + real_stats.steals + real_stats.blocks \
            + real_stats.field_goals_made + real_stats.three_pointers_made + real_stats.free_throws_made
    field_goals_missed = real_stats.field_goals_attempted - real_stats.field_goals_made
    three_pointers_missed = real_stats.three_pointers_attempted - real_stats.three_pointers_made
    free_throws_missed = real_stats.free_throws_attempted - real_stats.free_throws_made
    malus = field_goals_missed + three_pointers_missed + free_throws_missed + real_stats.turnovers

    return GameTTFLStats(bonus=bonus, malus=malus)


def game_stats(line: Tag):
    cells = line.select("td")
    points = int(cells[13].text)
    rebounds = int(cells[6].text)
    assists = int(cells[7].text)
    steals = int(cells[8].text)
    blocks = int(cells[9].text)
    field_goals = cells[1].text
    (field_goals_made, field_goals_attempted) = [int(s) for s in field_goals.split("-")]
    three_pointers = cells[2].text
    (three_pointers_made, three_pointers_attempted) = [int(s) for s in three_pointers.split("-")]
    free_throws = cells[3].text
    (free_throws_made, free_throws_attempted) = [int(s) for s in free_throws.split("-")]
    turnovers = int(cells[10].text)

    return GameRealStats(
        points=points,
        rebounds=rebounds,
        assists=assists,
        steals=steals,
        blocks=blocks,
        field_goals_made=field_goals_made,
        field_goals_attempted=field_goals_attempted,
        three_pointers_made=three_pointers_made,
        three_pointers_attempted=three_pointers_attempted,
        free_throws_made=free_throws_made,
        free_throws_attempted=free_throws_attempted,
        turnovers=turnovers
    )


def to_emoji(ttfl_score: int) -> Emoji:
    match ttfl_score:
        case _ if ttfl_score < 10:
            return Emoji.face_vomiting
        case _ if ttfl_score < 20:
            return Emoji.expressionless
        case _ if ttfl_score < 30:
            return Emoji.face_with_rolling_eyes
        case _ if ttfl_score < 35:
            return Emoji.unamused
        case _ if ttfl_score < 40:
            return Emoji.sweat_smile
        case _ if ttfl_score < 45:
            return Emoji.blush
        case _ if ttfl_score < 50:
            return Emoji.smile
        case _ if ttfl_score < 60:
            return Emoji.sunglasses
        case _ if ttfl_score < 80:
            return Emoji.heart_eyes
        case _:
            return Emoji.exploding_head
