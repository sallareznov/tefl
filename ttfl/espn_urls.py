from ttfl.teams import Team

all_teams_injuries: str = f"https://www.espn.com/nba/injuries"
scoreboard: str = f"https://www.espn.com/nba/scoreboard"
def team_stats(team: Team) -> str: return f"https://www.espn.com/nba/team/stats/_/name/{team.short_name}/{team.name}"
def team_injuries(team: Team) -> str: return f"https://www.espn.com/nba/team/injuries/_/name/{team.short_name}/{team.name}"
def team_roster(team: Team) -> str: return f"https://www.espn.com/nba/team/roster/_/name/{team.short_name}/{team.name}"
