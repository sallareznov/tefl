import re
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from json import JSONDecodeError

from nba_api.live.nba.endpoints.boxscore import BoxScore
from nba_api.live.nba.endpoints.scoreboard import ScoreBoard
from tinyhtml import h, _h, raw

import games
from emojis import Emoji
from games import GameRealStats, GameLocation
from teams import Team


class PlayerStatus(Enum):
    ON_COURT = Emoji.stadium
    ON_BENCH = Emoji.chair
    OUT = Emoji.not_permitted

    @staticmethod
    def from_live_game(player: dict):
        if "notPlayingReason" in player:
            return PlayerStatus.OUT
        if player["oncourt"] == "1":
            return PlayerStatus.ON_COURT
        else:
            return PlayerStatus.ON_BENCH

    def html(self) -> raw:
        return self.value.html()


@dataclass
class LiveGame:
    game_id: str
    home_team_tricode: str
    away_team_tricode: str


@dataclass
class PlayerLiveGameInfo:
    name: str
    team: Team
    ttfl_score: int
    minutes_played: int
    team_score: int
    status: PlayerStatus
    personal_fouls: int
    technical_fouls: int
    location: GameLocation
    opponent_team: Team
    opponent_team_score: int
    game_status: str

    def name_html(self):
        return self.team.logo_html(), " ", self.name

    def opponent_team_html(self):
        return self.location.emoji().html(), " ", self.opponent_team.nickname()

    def game_score_html(self):
        match self.location:
            case GameLocation.HOME:
                return self.opponent_team.logo_html(), f" {self.opponent_team_score} - {self.team_score} ", self.team.logo_html()
            case GameLocation.AWAY:
                return self.team.logo_html(), f" {self.team_score} - {self.opponent_team_score} ", self.opponent_team.logo_html()

    def minutes_played_html(self):
        return self.minutes_played, " ", Emoji.stopwatch.html()

    def fouls_html(self): return f"{self.personal_fouls} ({self.technical_fouls})"

    def ttfl_score_html(self) -> _h:
        return h("span", style="font-weight:bold;")(self.ttfl_score)


def live_ttfl_scores() -> list[PlayerLiveGameInfo]:
    live_games = [live_game_info(game) for game in ScoreBoard().get_dict()["scoreboard"]["games"]]
    all_scores = list(chain(*[scores_for_game(live_game) for live_game in live_games]))
    all_scores_sorted_by_ttfl_score_descending = sorted(all_scores, key=lambda ps: ps.ttfl_score, reverse=True)
    return all_scores_sorted_by_ttfl_score_descending


def live_game_info(game: dict) -> LiveGame:
    return LiveGame(
        game["gameId"],
        game["homeTeam"]["teamTricode"],
        game["awayTeam"]["teamTricode"]
    )


def scores_for_game(live_game: LiveGame) -> list[PlayerLiveGameInfo]:
    try:
        game = BoxScore(live_game.game_id).get_dict()["game"]
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


def team_scores(
        team: dict,
        team_score: int,
        opponent_tricode: str,
        opponent_team_score: int,
        location: GameLocation,
        game_status: str
) -> list[PlayerLiveGameInfo]:
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
) -> PlayerLiveGameInfo:
    name = player["nameI"]
    player_status = PlayerStatus.from_live_game(player)

    statistics = player["statistics"]
    minutes_played = int(re.findall("\d{2}", statistics["minutesCalculated"])[0])
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


    stats = GameRealStats(
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

    ttfl_stats = games.game_ttfl_stats(stats)

    team = Team.with_nba_abbreviation(team_tricode)
    opponent_team = Team.with_nba_abbreviation(opponent_tricode)

    return PlayerLiveGameInfo(
        name=name,
        team=team,
        team_score=team_score,
        opponent_team=opponent_team,
        opponent_team_score=opponent_team_score,
        location=location,
        minutes_played=minutes_played,
        ttfl_score=ttfl_stats.score,
        game_status=game_status,
        status=player_status,
        personal_fouls=personal_fouls,
        technical_fouls=technical_fouls
    )
