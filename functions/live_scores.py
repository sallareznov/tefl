import re
from itertools import chain
from json import JSONDecodeError

from nba_api.live.nba.endpoints.boxscore import BoxScore
from nba_api.live.nba.endpoints.scoreboard import ScoreBoard

from data.game_location import GameLocation
from data.game_stats import GameStats
from data.game_ttfl_stats import GameTTFLStats
from data.player_live_game import PlayerLiveGame
from data.player_status import PlayerStatus
from data.player_ttfl_score import PlayerTTFLScore
from data.team import team_with_nba_abbreviation


def live_ttfl_scores() -> list[PlayerLiveGame]:
    live_games = [game["gameId"] for game in ScoreBoard().get_dict()["scoreboard"]["games"]]
    players_live_games = list(chain(*[scores_for_game(live_game) for live_game in live_games]))
    return sorted(players_live_games, key=lambda live_game: live_game.ttfl_score, reverse=True)


def scores_for_game(game_id: str) -> list[PlayerLiveGame]:
    try:
        game = BoxScore(game_id).get_dict()["game"]
        game_status = game["gameStatusText"]
        home_team = game["homeTeam"]
        away_team = game["awayTeam"]
        home_team_tricode = home_team["teamTricode"]
        away_team_tricode = away_team["teamTricode"]
        home_team_score = home_team["score"]
        away_team_score = away_team["score"]

        home_team_scores = team_scores(
            home_team, home_team_score, away_team_tricode, away_team_score, GameLocation.HOME, game_status
        )
        away_team_scores = team_scores(
            away_team, away_team_score, home_team_tricode, home_team_score, GameLocation.AWAY, game_status
        )

        return home_team_scores + away_team_scores
    except JSONDecodeError:
        return []


def team_scores_bis(team: dict) -> list[PlayerTTFLScore]:
    return [player_live_score_bis(player) for player in team["players"]]


def player_live_score_bis(player: dict) -> PlayerTTFLScore:
    name = player["nameI"]
    position = player.get("position", "Bench")
    ttfl_score = player_ttfl_score(player["statistics"])

    return PlayerTTFLScore(
        name=name,
        position=position,
        ttfl_score=ttfl_score
    )


def player_ttfl_score(statistics: dict) -> int:
    minutes = int(re.findall("\d{2}", statistics["minutesCalculated"])[0])
    points = statistics["points"]
    rebounds = statistics["reboundsTotal"]
    assists = statistics["assists"]
    steals = statistics["steals"]
    blocks = statistics["blocks"]
    field_goals_made = statistics["fieldGoalsMade"]
    field_goals_attempted = statistics["fieldGoalsAttempted"]
    three_pointers_made = statistics["threePointersMade"]
    three_pointers_attempted = statistics["threePointersAttempted"]
    free_throws_made = statistics["freeThrowsMade"]
    free_throws_attempted = statistics["freeThrowsAttempted"]
    turnovers = statistics["turnovers"]

    stats = GameStats(
        minutes=minutes,
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

    return GameTTFLStats(stats).score


def team_scores(
        team: dict,
        team_score: int,
        opponent_tricode: str,
        opponent_team_score: int,
        location: GameLocation,
        game_status: str
) -> list[PlayerLiveGame]:
    return [
        player_live_score(
            player, team["teamTricode"], team_score, opponent_tricode, opponent_team_score, location, game_status
        )
        for player in team["players"]
    ]


def player_live_score(
        player: dict,
        team_tricode: str,
        team_score: int,
        opponent_tricode: str,
        opponent_team_score: int,
        location: GameLocation,
        game_status: str
) -> PlayerLiveGame:
    nameI = player["nameI"]
    full_name = player["name"]
    player_status = PlayerStatus.of_player(player)

    statistics = player["statistics"]
    minutes = int(re.findall("\d{2}", statistics["minutesCalculated"])[0])
    points = statistics["points"]
    rebounds = statistics["reboundsTotal"]
    assists = statistics["assists"]
    steals = statistics["steals"]
    blocks = statistics["blocks"]
    field_goals_made = statistics["fieldGoalsMade"]
    field_goals_attempted = statistics["fieldGoalsAttempted"]
    three_pointers_made = statistics["threePointersMade"]
    three_pointers_attempted = statistics["threePointersAttempted"]
    free_throws_made = statistics["freeThrowsMade"]
    free_throws_attempted = statistics["freeThrowsAttempted"]
    turnovers = statistics["turnovers"]
    personal_fouls = statistics["foulsPersonal"]
    technical_fouls = statistics["foulsTechnical"]

    stats = GameStats(
        minutes=minutes,
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

    ttfl_stats = GameTTFLStats(stats)

    team = team_with_nba_abbreviation(team_tricode)
    opponent_team = team_with_nba_abbreviation(opponent_tricode)

    return PlayerLiveGame(
        nameI=nameI,
        full_name=full_name,
        team=team,
        team_score=team_score,
        opponent_team=opponent_team,
        opponent_team_score=opponent_team_score,
        location=location,
        minutes_played=minutes,
        ttfl_score=ttfl_stats.score,
        game_status=game_status,
        status=player_status,
        personal_fouls=personal_fouls,
        technical_fouls=technical_fouls
    )
