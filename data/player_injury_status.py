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
        print(f"status = {status}")
        l = [s for s in PlayerInjuryStatus if s.value == status]
        if l:
            return l[0]
        else:
            return PlayerInjuryStatus.UNKNOWN
