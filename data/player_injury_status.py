from enum import Enum


class PlayerInjuryStatus(Enum):
    OUT = "Out"
    DOUBTFUL = "Doubtful"
    QUESTIONABLE = "Questionable"
    PROBABLE = "Probable"
    AVAILABLE = "Available"
    UNKNOWN = "Unknown"

    @staticmethod
    def with_status(status: str):
        return next(iter([s for s in PlayerInjuryStatus if s.value == status]), PlayerInjuryStatus.UNKNOWN)
