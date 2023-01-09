from enum import Enum

from nba_api.stats.static.teams import find_team_by_abbreviation
from tinyhtml import h


class Team(Enum):
    """
        nba abbreviation, espn abbreviation, ball-dont-lie id, primary color, secondary color, stats-muse uri
    """
    CELTICS = "BOS", "BOS", 2, "#007A33", "#FFFFFF"
    NETS = "BKN", "BKN", 3, "#707372", "#FFFFFF"
    KNICKS = "NYK", "NY", 20, "#003DA5", "#FFFFFF"
    SIXERS = "PHI", "PHI", 23, "#003DA5", "#FFFFFF"
    RAPTORS = "TOR", "TOR", 28, "#BA0C2F", "#FFFFFF"
    BULLS = "CHI", "CHI", 5, "#BA0C2F", "#FFFFFF"
    CAVALIERS = "CLE", "CLE", 6, "#6F263D", "#FFB81C"
    PISTONS = "DET", "DET", 9, "#1D428A", "#FFFFFF"
    PACERS = "IND", "IND", 12, "#041E42", "#FFC72C"
    BUCKS = "MIL", "MIL", 17, "#2C5234", "#DDCBA4"
    HAWKS = "ATL", "ATL", 1, "#C8102E", "#FFFFFF"
    HORNETS = "CHA", "CHA", 4, "#00778B", "#FFFFFF"
    HEAT = "MIA", "MIA", 16, "#862633", "#FFFFFF"
    MAGIC = "ORL", "ORL", 22, "#0057B8", "#FFFFFF"
    WIZARDS = "WAS", "WSH", 30, "#C8102E", "#FFFFFF"
    NUGGETS = "DEN", "DEN", 8, "#0C2340", "#FFC72C"
    WOLVES = "MIN", "MIN", 18, "#0C2340", "#FFFFFF"
    THUNDER = "OKC", "OKC", 21, "#0072CE", "#FFFFFF"
    BLAZERS = "POR", "POR", 25, "#C8102E", "#FFFFFF"
    JAZZ = "UTA", "UTAH", 29, "#52199F", "#EDE335"
    WARRIORS = "GSW", "GS", 10, "#1D4289", "#FFC72C"
    CLIPPERS = "LAC", "LAC", 13, "#1D428A", "#FFFFFF"
    LAKERS = "LAL", "LAL", 14, "#582C83", "#FFC72C"
    SUNS = "PHX", "PHX", 24, "#201747", "#FFFFFF"
    KINGS = "SAC", "SAC", 26, "#582C83", "#FFFFFF"
    MAVERICKS = "DAL", "DAL", 7, "#0050B5", "#FFFFFF"
    ROCKETS = "HOU", "HOU", 11, "#BA0C2F", "#FFFFFF"
    GRIZZLIES = "MEM", "MEM", 15, "#7D9BC0", "#0C2340"
    PELICANS = "NOP", "NO", 19, "#0C2340", "#FFFFFF"
    SPURS = "SAS", "SA", 27, "#8D9093", "#010101"

    def nba_abbreviation(self): return self.value[0]

    def espn_abbreviation(self): return self.value[1]

    def bdl_id(self): return self.value[2]

    def primary_color(self): return self.value[3]

    def secondary_color(self): return self.value[4]

    def team(self): return find_team_by_abbreviation(self.nba_abbreviation())

    def logo2525_html(self) -> h: return h("img", src=self.logo2525())

    def logo3535_html(self) -> h: return h("img", src=self.logo3535())

    def logo3535(self):
        return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{self.espn_abbreviation().lower()}.png&h=35&w=35"

    def logo2525(self) -> str:
        return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{self.espn_abbreviation().lower()}.png&h=25&w=25"

    def nickname(self) -> str: return self.team()["nickname"]

    def full_name(self) -> str: return self.team()["full_name"]

    def html_with_nickname(self): return self.logo2525_html(), " ", self.nickname()

    def html_with_full_name(self): return self.logo2525_html(), " ", self.full_name()


def team_with_nba_abbreviation(abbreviation: str) -> Team:
    return [team for team in list(Team) if team.nba_abbreviation() == abbreviation][0]


def team_with_bdl_id(bdl_id: str) -> Team: return [team for team in list(Team) if team.bdl_id() == bdl_id][0]


def team_logo_html(abbreviation: str) -> h: return team_with_nba_abbreviation(abbreviation).logo2525_html()
