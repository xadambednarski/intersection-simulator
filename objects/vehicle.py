from dataclasses import dataclass
from enum import Enum


class Direction(str, Enum):
    STRAIGHT = 1
    LEFT = 2
    RIGHT = 3


@dataclass
class Vehicle:
    id: int
    direction: Direction
