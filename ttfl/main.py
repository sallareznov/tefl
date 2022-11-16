import asyncio

from ttfl import rosters, teams

if __name__ == '__main__':
    all_rosters = asyncio.run(rosters.all_rosters(teams.all_nba_teams))
    print(all_rosters)
