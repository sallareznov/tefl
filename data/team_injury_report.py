from dataclasses import dataclass

from tinyhtml import _h, h, raw

from data.game_location import GameLocation
from data.injured_player import InjuredPlayer
from data.player_injury_status import PlayerInjuryStatus
from data.team import Team
from data.team_injury_report_status import TeamInjuryReportStatus


@dataclass
class TeamInjuryReport:
    team: Team
    opponent: Team
    location: GameLocation
    status: TeamInjuryReportStatus
    injured_players: list[InjuredPlayer]

    def __init__(self, team: Team, opponent: Team, location: GameLocation, status: TeamInjuryReportStatus):
        self.team = team
        self.opponent = opponent
        self.location = location
        self.status = status
        self.injured_players = []

    def add_player(self, name: str, status: str, reason: str):
        self.injured_players.append(
            InjuredPlayer(
                name=name,
                status=PlayerInjuryStatus.with_status(status),
                reason=reason
            )
        )

    def players_with_status(self, status: PlayerInjuryStatus):
        return [player for player in self.injured_players if player.status == status]

    def html_cell_for_injury_status(self, status: PlayerInjuryStatus) -> _h:
        return h("td", klass="text-center")(
            raw(f"{player.name}<br>") for player in self.players_with_status(status)
        )

    def matchup_html(self): return self.location.html_with_label(), " ", self.opponent.logo_html()
