from dataclasses import dataclass


@dataclass
class PlayerTTFLScore:
    name: str
    position: str
    ttfl_score: int
