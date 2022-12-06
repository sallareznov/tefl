injury_report = "https://official.nba.com/nba-injury-report-2022-23-season/"


def player_gamelog(uri: str) -> str: return f"https://www.basketball-reference.com{uri}/gamelog/2023"


def team_logo(team_short_name: str) -> str:
    return f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{team_short_name}.png&h=25&w=25"


def team_url(team_short_name: str) -> str:
    return f"https://www.basketball-reference.com/teams/{team_short_name}/2023.html"
