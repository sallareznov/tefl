from enum import Enum

from nba_api.stats.static.teams import find_team_by_abbreviation
from tinyhtml import h


class Team(Enum):
    """
        nba abbreviation, espn abbreviation, ball-dont-lie id
    """
    CELTICS = "BOS", "BOS", 2
    NETS = "BKN", "BKN", 3
    KNICKS = "NYK", "NY", 20
    SIXERS = "PHI", "PHI", 23
    RAPTORS = "TOR", "TOR", 28
    BULLS = "CHI", "CHI", 5
    CAVALIERS = "CLE", "CLE", 6
    PISTONS = "DET", "DET", 9
    PACERS = "IND", "IND", 12
    BUCKS = "MIL", "MIL", 17
    HAWKS = "ATL", "ATL", 1
    HORNETS = "CHA", "CHA", 4
    HEAT = "MIA", "MIA", 16
    MAGIC = "ORL", "ORL", 22
    WIZARDS = "WAS", "WSH", 30
    NUGGETS = "DEN", "DEN", 8
    WOLVES = "MIN", "MIN", 18
    THUNDER = "OKC", "OKC", 21
    BLAZERS = "POR", "POR", 25
    JAZZ = "UTA", "UTAH", 29
    WARRIORS = "GSW", "GS", 10
    CLIPPERS = "LAC", "LAC", 13
    LAKERS = "LAL", "LAL", 14
    SUNS = "PHX", "PHX", 24
    KINGS = "SAC", "SAC", 26
    MAVERICKS = "DAL", "DAL", 7
    ROCKETS = "HOU", "HOU", 11
    GRIZZLIES = "MEM", "MEM", 15
    PELICANS = "NOP", "NO", 19
    SPURS = "SAS", "SA", 27

    def nba_abbreviation(self): return self.value[0]

    def espn_abbreviation(self): return self.value[1]

    def team(self): return find_team_by_abbreviation(self.nba_abbreviation())

    def bdl_id(self): return self.value[2]

    def logo_html(self) -> h: return h("img", src=self.logo_url())

    def logo_url(self) -> str:
        return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{self.espn_abbreviation().lower()}.png&h=25&w=25"

    def nickname(self) -> str: return self.team()["nickname"]

    def full_name(self) -> str: return self.team()["full_name"]

    def html_with_nickname(self): return self.logo_html(), " ", self.nickname()

    def html_with_full_name(self): return self.logo_html(), " ", self.full_name()


def with_nba_abbreviation(abbreviation: str) -> Team:
    return [team for team in list(Team) if team.nba_abbreviation() == abbreviation][0]


def with_bdl_id(bdl_id: str) -> Team:
    return [team for team in list(Team) if team.bdl_id() == bdl_id][0]


def logo_html(abbreviation: str) -> h: return with_nba_abbreviation(abbreviation).logo_html()
