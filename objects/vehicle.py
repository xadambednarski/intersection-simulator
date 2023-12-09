from dataclasses import dataclass
from enum import Enum


class Direction(str, Enum):
    """Enumerating vehicles turn options"""

    STRAIGHT = 1
    LEFT = 2
    RIGHT = 3


@dataclass
class Vehicle:
    """Class of vehicle objects which are kind of a data containers"""

    id: int
    direction: Direction
