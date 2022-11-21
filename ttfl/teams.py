from enum import Enum

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag

from ttfl.players import Player


class Team(Enum):
    CELTICS = "Boston Celtics", "BOS"
    NETS = "Brooklyn Nets", "BKN"
    KNICKS = "New York Knicks", "NYK"
    SIXERS = "Philadelphia Sixers", "PHI"
    RAPTORS = "Toronto Raptors", "TOR"
    BULLS = "Chicago Bulls", "CHI"
    CAVALIERS = "Cleveland Cavaliers", "CLE"
    PISTONS = "Detroit Pistons", "DET"
    PACERS = "Indiana Pacers", "IND"
    BUCKS = "Milwaukee Bucks", "MIL"
    HAWKS = "Atlanta Hawks", "ATL"
    HORNETS = "Charlotte Hornets", "CHO"
    HEAT = "Miami Heat", "MIA"
    MAGIC = "Orlando Magic", "ORL"
    WIZARDS = "Washington Wizards", "WAS"
    NUGGETS = "Denver Nuggets", "DEN"
    WOLVES = "Minnesota Timberwolves", "MIN"
    THUNDER = "Oklahoma City Thunder", "OKC"
    BLAZERS = "Portland Trailblazers", "POR"
    JAZZ = "Utah Jazz", "UTA"
    WARRIORS = "Golden State Warriors", "GSW"
    CLIPPERS = "Los Angeles Clippers", "LAC"
    LAKERS = "Los Angeles Lakers", "LAL"
    SUNS = "Phoenix Suns", "PHX"
    KINGS = "Sacramento Kings", "SAC"
    MAVERICKS = "Dallas Mavericks", "DAL"
    ROCKETS = "Houston Rockets", "HOU"
    GRIZZLIES = "Memphis Grizzlies", "MEM"
    PELICANS = "New Orleans Pelicans", "NOP"
    SPURS = "San Antonio Spurs", "SAS"

    async def roster(self, session: ClientSession) -> list[Player]:
        team_roster_url: str = f"https://www.basketball-reference.com/teams/{self.value[1]}/2023.html"
        r = await session.request('GET', url=team_roster_url)
        text: str = await r.text()
        soup: BeautifulSoup = BeautifulSoup(text, "html.parser")

        return [self.extract_player_info(player) for player in soup.select("table#roster > tbody > tr")]

    @staticmethod
    def extract_player_info(player_tag: Tag) -> Player:
        player_name_tag = player_tag.select_one("td[data-stat='player']")
        player_profile_tag = player_name_tag.select_one("a")
        player_name = player_profile_tag.text
        player_profile_url = player_profile_tag.get("href")
        return Player(name=player_name, profile_url=player_profile_url)
