import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from pymonet.monad_try import Try
from requests import Response

from tefl.teams import teams_dict


def injuries(team_name: str):
    response: Response = requests.get(f"https://www.espn.com/nba/team/injuries/_/name/{team_name}")
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    injured_players: ResultSet[Tag] = soup.select(".Athlete")

    for player in injured_players:
        player_name = Try.of(lambda selector: player.select_one(selector).text, ".Athlete__PlayerName").get_or_else("")
        player_injury_status = Try.of(lambda selector: player.select_one(selector).text, ".TextStatus").get_or_else("")
        player_injury_info = Try.of(lambda selector: player.select_one(selector).text, ".pt3").get_or_else("")
        print(player_name)
        print(player_injury_status)
        print(player_injury_info)


if __name__ == '__main__':
    print(injuries("det"))
