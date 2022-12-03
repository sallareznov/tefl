from enum import Enum


# city, name, basketball reference id, espn id, nba id
class Team(Enum):
    CELTICS = "Boston", "Celtics", "BOS", "BOS", "BOS"
    NETS = "Brooklyn", "Nets", "BRK", "BKN", "BKN"
    KNICKS = "New York", "Knicks", "NYK", "NY", "NYK"
    SIXERS = "Philadelphia", "76ers", "PHI", "PHI", "PHI"
    RAPTORS = "Toronto", "Raptors", "TOR", "TOR", "TOR"
    BULLS = "Chicago", "Bulls", "CHI", "CHI", "CHI"
    CAVALIERS = "Cleveland", "Cavaliers", "CLE", "CLE", "CLE"
    PISTONS = "Detroit", "Pistons", "DET", "DET", "DET"
    PACERS = "Indiana", "Pacers", "IND", "IND", "IND"
    BUCKS = "Milwaukee", "Bucks", "MIL", "MIL", "MIL"
    HAWKS = "Atlanta", "Hawks", "ATL", "ATL", "ATL"
    HORNETS = "Charlotte", "Hornets", "CHO", "CHA", "CHA"
    HEAT = "Miami", "Heat", "MIA", "MIA", "MIA"
    MAGIC = "Orlando", "Magic", "ORL", "ORL", "ORL"
    WIZARDS = "Washington", "Wizards", "WAS", "WSH", "WAS"
    NUGGETS = "Denver", "Nuggets", "DEN", "DEN", "DEN"
    WOLVES = "Minnesota", "Timberwolves", "MIN", "MIN", "MIN"
    THUNDER = "Oklahoma City", "Thunder", "OKC", "OKC", "OKC"
    BLAZERS = "Portland", "Trail Blazers", "POR", "POR", "POR"
    JAZZ = "Utah", "Jazz", "UTA", "UTAH", "UTA"
    WARRIORS = "Golden State", "Warriors", "GSW", "GS", "GSW"
    CLIPPERS = "Los Angeles", "Clippers", "LAC", "LAC", "LAC"
    LAKERS = "Los Angeles", "Lakers", "LAL", "LAL", "LAL"
    SUNS = "Phoenix", "Suns", "PHO", "PHX", "PHX"
    KINGS = "Sacramento", "Kings", "SAC", "SAC", "SAC"
    MAVERICKS = "Dallas", "Mavericks", "DAL", "DAL", "DAL"
    ROCKETS = "Houston", "Rockets", "HOU", "HOU", "HOU"
    GRIZZLIES = "Memphis", "Grizzlies", "MEM", "MEM", "MEM"
    PELICANS = "New Orleans", "Pelicans", "NOP", "NO", "NOP"
    SPURS = "San Antonio", "Spurs", "SAS", "SA", "SAS"

    def logo(self) -> str:
        return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{self.value[3].lower()}.png&h=25&w=25"

    def full_name(self) -> str:
        return f"{self.value[0]} {self.value[1]}"

    @staticmethod
    def with_basketball_reference_id(short_name: str):
        return next(team for team in list(Team) if team.value[2] == short_name)

    @staticmethod
    def with_nba_id(short_name: str):
        return next(team for team in list(Team) if team.value[4] == short_name)

    def equals(self, name: str) -> bool:
        return " ".join([self.value[0], self.value[1]]) == name
