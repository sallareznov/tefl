from itertools import chain

import requests
from bs4 import BeautifulSoup, Tag
import scores


def scoreboard_links() -> list[str]:
    scoreboard_url = "https://www.espn.com/nba/scoreboard"
    response = requests.get(scoreboard_url)
    soup = BeautifulSoup(response.text, "html.parser")

    boxscore_tags = soup.find_all("a", text="Box Score")

    return [b.get("href") for b in boxscore_tags]


def players_ttfl_scores(boxscore_link: str) -> list[tuple[str, int, str]]:
    response = requests.get(f"https://www.espn.com{boxscore_link}")
    soup = BeautifulSoup(response.text, "html.parser")

    time = soup.select_one("div[class~=Gamestrip__Time]").text
    player_names = soup.select("div[class~=Boxscore] > div[class~=flex] > table")
    stat_lines = soup.select("div[class~=Boxscore] > div[class~=flex] > div[class~=relative]")

    players = [get_players(p) for p in player_names]
    ttfl_scores = [scores.get_ttfl_scores(s) for s in stat_lines]

    players_with_scores = list(chain(*[list(zip(p, s)) for (p, s) in list(zip(players, ttfl_scores))]))
    players_with_scores_and_time = [(player, score, time) for (player, score) in players_with_scores]

    return players_with_scores_and_time


def get_players(names: Tag) -> list[str]:
    return [player.text for player in names.select("tr a")]




