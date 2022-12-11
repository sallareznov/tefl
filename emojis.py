from enum import Enum

from tinyhtml import raw


# https://www.w3schools.com/charsets/ref_emoji.asp
class Emoji(Enum):
    airplane = 9992
    blush = 128522
    chair = 129681
    exploding_head = 129327
    expressionless = 128529
    face_vomiting = 129326
    face_with_rolling_eyes = 128580
    heart_eyes = 128525
    house = 127968
    not_permitted = 128683
    smile = 128516
    stadium = 127967
    stopwatch = 9201
    sunglasses = 128526
    sweat_smile = 128517
    unamused = 128530

    def html(self) -> raw: return raw(f" &#{self.value};")
