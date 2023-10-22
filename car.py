from dataclasses import dataclass
from enum import Enum

class Direction(str, Enum):
    STRAIGHT = 1
    LEFT = 2
    RIGHT = 3

@dataclass
class Car():
    id: int
    type: str
    direction: "Direction"