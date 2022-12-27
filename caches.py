from loguru import logger
from nba_api.stats.endpoints import CumeStatsPlayerGames

from games import Gamelog
from injury_reports import TeamInjuryReport
from live_scores import MatchupTTFLStats
from teams import Team


class Caches:
    latest_injury_report: list[TeamInjuryReport]
    gamelog_cache: dict[str, Gamelog]
    teams_gamelog_cache: dict[Team, list[MatchupTTFLStats]]

    def __init__(self):
        self.latest_injury_report = None
        self.gamelog_cache = {}
        self.teams_gamelog_cache = {}

    def get_latest_injury_report(self):
        if self.latest_injury_report:
            logger.info(f"getting latest injury report from cache")
        else:
            logger.info(f"no latest injury report in cache")
        return self.latest_injury_report

    def set_latest_injury_report(self, injury_report: list[TeamInjuryReport]):
        if not self.latest_injury_report:
            logger.info("set latest injury report in cache")
        self.latest_injury_report = injury_report

    def add_to_gamelog_cache(self, player_id: str, gamelog: Gamelog):
        if not self.gamelog_cache.get(player_id):
            logger.info(f"adding gamelog of player {player_id} to cache")
        self.gamelog_cache[player_id] = gamelog

    def add_to_teams_gamelog_cache(self, team: Team, stats: list[MatchupTTFLStats]):
        if not self.teams_gamelog_cache.get(team):
            logger.info(f"adding gamelog of team {team.nickname()} to cache")
        self.teams_gamelog_cache[team] = stats

    def get_gamelog_of_player(self, player_id: str):
        value = self.gamelog_cache.get(player_id)
        if value:
            logger.info(f"getting gamelog of player {player_id} from cache")
        else:
            logger.info(f"no gamelog for {player_id} in cache")
        return value

    def get_gamelog_for_team(self, team: Team):
        value = self.teams_gamelog_cache.get(team)
        if value:
            logger.info(f"getting gamelog of team {team.nickname()} from cache")
        else:
            logger.info(f"no gamelog for team {team.nickname()} in cache")
        return value

    def clear_latest_injury_report(self):
        logger.info("clearing latest injury report in cache")
        self.latest_injury_report = None

    def clear_gamelog_cache(self):
        logger.info("clearing gamelog in cache")
        self.gamelog_cache.clear()

    def clear_teams_gamelog_cache(self):
        logger.info("clearing team gamelog in cache")
        self.teams_gamelog_cache.clear()


#if __name__ == '__main__':
#    print(games)
