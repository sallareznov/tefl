from enum import Enum

from tinyhtml import h

import urls


class Team(Enum):
    """
        city, nickname, nba tricode, espn tricode
    """
    CELTICS = "Boston", "Celtics", "BOS", "BOS"
    NETS = "Brooklyn", "Nets", "BKN", "BKN"
    KNICKS = "New York", "Knicks", "NYK", "NY"
    SIXERS = "Philadelphia", "76ers", "PHI", "PHI"
    RAPTORS = "Toronto", "Raptors", "TOR", "TOR"
    BULLS = "Chicago", "Bulls", "CHI", "CHI"
    CAVALIERS = "Cleveland", "Cavaliers", "CLE", "CLE"
    PISTONS = "Detroit", "Pistons", "DET", "DET"
    PACERS = "Indiana", "Pacers", "IND", "IND"
    BUCKS = "Milwaukee", "Bucks", "MIL", "MIL"
    HAWKS = "Atlanta", "Hawks", "ATL", "ATL"
    HORNETS = "Charlotte", "Hornets", "CHA", "CHA"
    HEAT = "Miami", "Heat", "MIA", "MIA"
    MAGIC = "Orlando", "Magic", "ORL", "ORL"
    WIZARDS = "Washington", "Wizards", "WAS", "WSH"
    NUGGETS = "Denver", "Nuggets", "DEN", "DEN"
    WOLVES = "Minnesota", "Timberwolves", "MIN", "MIN"
    THUNDER = "Oklahoma City", "Thunder", "OKC", "OKC"
    BLAZERS = "Portland", "Trail Blazers", "POR", "POR"
    JAZZ = "Utah", "Jazz", "UTA", "UTAH"
    WARRIORS = "Golden State", "Warriors", "GSW", "GS"
    CLIPPERS = "LA", "Clippers", "LAC", "LAC"
    LAKERS = "Los Angeles", "Lakers", "LAL", "LAL"
    SUNS = "Phoenix", "Suns", "PHX", "PHX"
    KINGS = "Sacramento", "Kings", "SAC", "SAC"
    MAVERICKS = "Dallas", "Mavericks", "DAL", "DAL"
    ROCKETS = "Houston", "Rockets", "HOU", "HOU"
    GRIZZLIES = "Memphis", "Grizzlies", "MEM", "MEM"
    PELICANS = "New Orleans", "Pelicans", "NOP", "NO"
    SPURS = "San Antonio", "Spurs", "SAS", "SA"

    def logo(self) -> h: return h("img", src=urls.team_logo(self.espn_code().lower()))

    def city(self) -> str: return self.value[0]

    def nickname(self) -> str: return self.value[1]

    def full_name(self) -> str: return f"{self.city()} {self.nickname()}"

    def nba_code(self) -> str: return self.value[2]

    def espn_code(self) -> str: return self.value[3]

    def html_with_nickname(self): return self.logo(), " ", self.nickname()

    def html_with_full_name(self): return self.logo(), " ", self.full_name()

    @staticmethod
    def with_nba_tricode(short_name: str): return [team for team in list(Team) if team.nba_code() == short_name][0]

    def equals(self, name: str) -> bool: return self.full_name() == name
