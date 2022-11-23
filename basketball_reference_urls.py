def team_url(team_short_name: str) -> str:
    return f"https://www.basketball-reference.com/teams/{team_short_name}/2023.html"


def player_gamelog_url(uri: str) -> str:
    return f"https://www.basketball-reference.com{uri}/gamelog/2023"
