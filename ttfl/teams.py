from dataclasses import dataclass


@dataclass
class Team:
    short_name: str
    name: str


all_nba_teams = [
    # atlantic
    Team("bos", "boston-celtics"),
    Team("bkn", "brooklyn-nets"),
    Team("ny", "new-york-knicks"),
    Team("phi", "philadelphia-76ers"),
    Team("tor", "toronto-raptors"),

    # central
    Team("chi", "chicago-bulls"),
    Team("cle", "cleveland-cavaliers"),
    Team("det", "detroit-pistons"),
    Team("ind", "indiana-pacers"),
    Team("mil", "milwaukee-bucks"),

    # southeast
    Team("chi", "atlanta-hawks"),
    Team("cha", "charlotte-hornets"),
    Team("mia", "miami-heat"),
    Team("orl", "orlando-magic"),
    Team("wsh", "washington-wizards"),

    # northwest
    Team("den", "denver-nuggets"),
    Team("min", "minnesota-timberwolves"),
    Team("okc", "oklahoma-city-thunder"),
    Team("por", "portland-trail-blazers"),
    Team("utah", "utah-jazz"),

    # pacific
    Team("gs", "golden-state-warriors"),
    Team("lac", "los-angeles-clippers"),
    Team("lal", "los-angeles-lakers"),
    Team("phx", "phoenix-suns"),
    Team("sac", "sacramento-kings"),

    # southwest
    Team("dal", "dallas-mavericks"),
    Team("hou", "houston-rockets"),
    Team("mem", "memphis-grizzlies"),
    Team("no", "new-orleans-pelicans"),
    Team("sa", "san-antonio-spurs")
]

teams_dict = {team.short_name: team for team in all_nba_teams}
