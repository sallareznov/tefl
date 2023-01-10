from dataclasses import dataclass

from tinyhtml import _h, h

from data.game_location import GameLocation
from data.player_status import PlayerStatus
from data.team import Team
from emojis import Emoji


@dataclass
class PlayerLiveGame:
    nameI: str
    full_name: str
    team: Team
    ttfl_score: int
    minutes_played: int
    team_score: int
    status: PlayerStatus
    personal_fouls: int
    technical_fouls: int
    location: GameLocation
    opponent_team: Team
    opponent_team_score: int
    game_status: str

    def name_html(self):
        return h("span", title=self.full_name)(self.team.logo2525_html(), " ", self.nameI)

    def opponent_team_html(self):
        return self.location.emoji().html(), " ", self.opponent_team.nickname()

    def game_score_html(self):
        match self.location:
            case GameLocation.HOME:
                return self.opponent_team.logo2525_html(), f" {self.opponent_team_score} - {self.team_score} ", self.team.logo2525_html()
            case GameLocation.AWAY:
                return self.team.logo2525_html(), f" {self.team_score} - {self.opponent_team_score} ", self.opponent_team.logo2525_html()

    def minutes_played_html(self):
        return self.minutes_played, " ", Emoji.stopwatch.html()

    def fouls_html(self):
        return f"{self.personal_fouls} ({self.technical_fouls})"

    def ttfl_score_html(self) -> _h:
        return h("span", style="font-weight:bold;")(self.ttfl_score)
