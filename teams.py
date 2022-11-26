from enum import Enum


# city, name, basketball reference id, espn id
class Team(Enum):
    CELTICS = "Boston", "Celtics", "BOS", "BOS"
    NETS = "Brooklyn", "Nets", "BRK", "BKN"
    KNICKS = "New York", "Knicks", "NYK", "NY"
    SIXERS = "Philadelphia", "Sixers", "PHI", "PHI"
    RAPTORS = "Toronto", "Raptors", "TOR", "TOR"
    BULLS = "Chicago", "Bulls", "CHI", "CHI"
    CAVALIERS = "Cleveland", "Cavaliers", "CLE", "CLE"
    PISTONS = "Detroit", "Pistons", "DET", "DET"
    PACERS = "Indiana", "Pacers", "IND", "IND"
    BUCKS = "Milwaukee", "Bucks", "MIL", "MIL"
    HAWKS = "Atlanta", "Hawks", "ATL", "ATL"
    HORNETS = "Charlotte", "Hornets", "CHO", "CHA"
    HEAT = "Miami", "Heat", "MIA", "MIA"
    MAGIC = "Orlando", "Magic", "ORL", "ORL"
    WIZARDS = "Washington", "Wizards", "WAS", "WSH"
    NUGGETS = "Denver", "Nuggets", "DEN", "DEN"
    WOLVES = "Minnesota", "Timberwolves", "MIN", "MIN"
    THUNDER = "Oklahoma City", "Thunder", "OKC", "OKC"
    BLAZERS = "Portland", "Trailblazers", "POR", "POR"
    JAZZ = "Utah", "Jazz", "UTA", "UTAH"
    WARRIORS = "Golden State", "Warriors", "GSW", "GS"
    CLIPPERS = "Los Angeles", "Clippers", "LAC", "LAC"
    LAKERS = "Los Angeles", "Lakers", "LAL", "LAL"
    SUNS = "Phoenix", "Suns", "PHO", "PHX"
    KINGS = "Sacramento", "Kings", "SAC", "SAC"
    MAVERICKS = "Dallas", "Mavericks", "DAL", "DAL"
    ROCKETS = "Houston", "Rockets", "HOU", "HOU"
    GRIZZLIES = "Memphis", "Grizzlies", "MEM", "MEM"
    PELICANS = "New Orleans", "Pelicans", "NOP", "NO"
    SPURS = "San Antonio", "Spurs", "SAS", "SA"

    def logo(self) -> str:
        return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{self.value[3].lower()}.png&h=25&w=25"
