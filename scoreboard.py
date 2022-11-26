from itertools import chain

import pandas
import requests
from bs4 import BeautifulSoup, Tag
from numpy import ndarray

import scores
from games import GameRealStats, GameLocation
from teams import Team


def scoreboard_links() -> list[str]:
    scoreboard_url = "https://www.espn.com/nba/scoreboard"
    response = requests.get(scoreboard_url)
    soup = BeautifulSoup(response.text, "html.parser")

    boxscore_tags = soup.find_all("a", text="Box Score")

    return [bt.get("href") for bt in boxscore_tags]


def ttfl_scores_for_game(boxscore_link: str) -> list[tuple[str, int, int, Team, GameLocation, Team]]:
    tables = pandas.read_html(f"https://www.espn.com{boxscore_link}")

    away_team: Team = next(team for team in list(Team) if team.value[3] in tables[0].values[0][0])
    home_team: Team = next(team for team in list(Team) if team.value[3] in tables[0].values[1][0])

    away_team_stats: list[tuple[ndarray[str], ndarray[str]]] = list(zip(tables[1].values, tables[2].values))
    home_team_stats: list[tuple[ndarray[str], ndarray[str]]] = list(zip(tables[3].values, tables[4].values))

    away_team_ttfl_scores: list[tuple[str, int, int, Team, GameLocation, Team]] = \
        ttfl_scores_for_team(
            away_team,
            away_team_stats,
            GameLocation.AWAY,
            home_team
        )

    home_team_ttfl_scores: list[tuple[str, int, int, Team, GameLocation, Team]] = \
        ttfl_scores_for_team(
            home_team,
            home_team_stats,
            GameLocation.HOME,
            away_team
        )

    return list(chain(*[away_team_ttfl_scores, home_team_ttfl_scores]))


def ttfl_scores_for_team(
        team: Team,
        stats: list[tuple[ndarray[str], ndarray[str]]],
        location: GameLocation,
        opponent: Team
) -> list[tuple[str, int, int, Team, GameLocation, Team]]:
    players_involved = [
        x for x in stats
        if x[0][0] not in ["starters", "bench", "team"]
        if x[1][0].isdigit()
    ]

    return [player_gamelog(player) + (team, location, opponent) for player in players_involved]


def get_players(names: Tag) -> list[str]:
    return [player.text for player in names.select("tr a")]


def player_gamelog(s: tuple[ndarray[str], ndarray[str]]) -> tuple[str, int, int]:
    player_name = " ".join(s[0][0].split(" ")[:-1])
    minutes_played = int(s[1][0])
    points = int(s[1][13])
    rebounds = int(s[1][6])
    assists = int(s[1][7])
    steals = int(s[1][8])
    blocks = int(s[1][9])
    (free_throws_made, free_throws_attempted) = [int(ft) for ft in s[1][3].split("-")]
    (three_pointers_made, three_pointers_attempted) = [int(tp) for tp in s[1][2].split("-")]
    (field_goals_made, field_goals_attempted) = [int(fg) for fg in s[1][1].split("-")]
    turnovers = int(s[1][10])

    real_stats = GameRealStats(
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

    return player_name, scores.game_ttfl_stats(real_stats).score, minutes_played
