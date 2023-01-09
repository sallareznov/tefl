from enum import Enum

from nba_api.stats.static.teams import find_team_by_abbreviation
from tinyhtml import h


class Team(Enum):
    """
        nba abbreviation, espn abbreviation, ball-dont-lie id, stats-muse uri
    """
    CELTICS = "BOS", "BOS", 2, "boston-celtics-1"
    NETS = "BKN", "BKN", 3, "brooklyn-nets-33"
    KNICKS = "NYK", "NY", 20, "new-york-knicks-5"
    SIXERS = "PHI", "PHI", 23, "philadelphia-76ers-21"
    RAPTORS = "TOR", "TOR", 28, "toronto-raptors-51"
    BULLS = "CHI", "CHI", 5, "chicago-bulls-25"
    CAVALIERS = "CLE", "CLE", 6, "cleveland-cavaliers-42"
    PISTONS = "DET", "DET", 9, "detroit-pistons-13"
    PACERS = "IND", "IND", 12, "indiana-pacers-30"
    BUCKS = "MIL", "MIL", 17, "milwaukee-bucks-39"
    HAWKS = "ATL", "ATL", 1, "atlanta-hawks-22"
    HORNETS = "CHA", "CHA", 4, "charlotte-hornets-53"
    HEAT = "MIA", "MIA", 16, "miami-heat-48"
    MAGIC = "ORL", "ORL", 22, "orlando-magic-50"
    WIZARDS = "WAS", "WSH", 30, "washington-wizards-24"
    NUGGETS = "DEN", "DEN", 8, "denver-nuggets-28"
    WOLVES = "MIN", "MIN", 18, "minnesota-timberwolves-49"
    THUNDER = "OKC", "OKC", 21, "oklahoma-city-thunder-38"
    BLAZERS = "POR", "POR", 25, "portland-trail-blazers-43"
    JAZZ = "UTA", "UTAH", 29, "utah-jazz-45"
    WARRIORS = "GSW", "GS", 10, "golden-state-warriors-6"
    CLIPPERS = "LAC", "LAC", 13, "l.a.-clippers-41"
    LAKERS = "LAL", "LAL", 14, "los-angeles-lakers-15"
    SUNS = "PHX", "PHX", 24, "phoenix-suns-40"
    KINGS = "SAC", "SAC", 26, "sacramento-kings-16"
    MAVERICKS = "DAL", "DAL", 7, "dallas-mavericks-46"
    ROCKETS = "HOU", "HOU", 11, "houston-rockets-37"
    GRIZZLIES = "MEM", "MEM", 15, "memphis-grizzlies-52"
    PELICANS = "NOP", "NO", 19, "new-orleans-pelicans-47"
    SPURS = "SAS", "SA", 27, "san-antonio-spurs-27"

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


def team_with_nba_abbreviation(abbreviation: str) -> Team:
    return [team for team in list(Team) if team.nba_abbreviation() == abbreviation][0]


def team_with_bdl_id(bdl_id: str) -> Team: return [team for team in list(Team) if team.bdl_id() == bdl_id][0]


def team_logo_html(abbreviation: str) -> h: return team_with_nba_abbreviation(abbreviation).logo_html()
