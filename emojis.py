from enum import Enum

from tinyhtml import raw


# https://www.w3schools.com/charsets/ref_emoji.asp
class Emoji(Enum):
    airplane = 9992
    blush = 128522
    exploding_head = 129327
    expressionless = 128529
    face_vomiting = 129326
    face_with_rolling_eyes = 128580
    heart_eyes = 128525
    house = 127968
    smile = 128516
    stopwatch = 9201
    sunglasses = 128526
    sweat_smile = 128517
    unamused = 128530

    def html(self):
        return raw(f" &#{self.value};")


def from_ttfl_score(ttfl_score: int) -> Emoji:
    match ttfl_score:
        case _ if ttfl_score < 10:
            return Emoji.face_vomiting
        case _ if ttfl_score < 20:
            return Emoji.expressionless
        case _ if ttfl_score < 30:
            return Emoji.face_with_rolling_eyes
        case _ if ttfl_score < 35:
            return Emoji.unamused
        case _ if ttfl_score < 40:
            return Emoji.sweat_smile
        case _ if ttfl_score < 45:
            return Emoji.blush
        case _ if ttfl_score < 50:
            return Emoji.smile
        case _ if ttfl_score < 60:
            return Emoji.sunglasses
        case _ if ttfl_score < 80:
            return Emoji.heart_eyes
        case _:
            return Emoji.exploding_head
