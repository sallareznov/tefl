from dataclasses import dataclass

from data.player_injury_status import PlayerInjuryStatus


@dataclass
class InjuredPlayer:
    name: str
    status: PlayerInjuryStatus
    reason: str
    # premium: bool