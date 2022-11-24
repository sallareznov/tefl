from itertools import chain

import requests
from bs4 import BeautifulSoup, Tag

import games
from games import GameRealStats


def scoreboard_links() -> list[str]:
    scoreboard_url = "https://www.espn.com/nba/scoreboard"
    response = requests.get(scoreboard_url)
    soup = BeautifulSoup(response.text, "html.parser")

    boxscore_tags = soup.find_all("a", text="Box Score")

    return [b.get("href") for b in boxscore_tags]


def players_ttfl_score(boxscore_link: str) -> list[tuple[str, int, str]]:
    response = requests.get(f"https://www.espn.com{boxscore_link}")
    soup = BeautifulSoup(response.text, "html.parser")

    time = soup.select_one("div[class~=Gamestrip__Time]").text
    player_names = soup.select("div[class~=Boxscore] > div[class~=flex] > table")
    stat_lines = soup.select("div[class~=Boxscore] > div[class~=flex] > div[class~=relative]")

    players = [get_players(p) for p in player_names]
    scores = [get_ttfl_scores(s) for s in stat_lines]

    players_with_scores = list(chain(*[list(zip(p, s)) for (p, s) in list(zip(players, scores))]))
    players_with_scores_and_time = [(player, score, time) for (player, score) in players_with_scores]

    return players_with_scores_and_time


def get_players(names: Tag) -> list[str]:
    return [player.text for player in names.select("tr a")]


def get_ttfl_scores(boxscore: Tag):
    lines = boxscore.select("tr[class~=Table__TR]")
    stat_lines = [line for line in lines if line.select("td")[0].text.isdigit()]
    stats = [game_stats(line) for line in stat_lines]
    ttfl_stats = [games.game_ttfl_stats(s) for s in stats]

    return [s.score for s in ttfl_stats]


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
