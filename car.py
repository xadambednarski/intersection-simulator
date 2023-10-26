from dataclasses import dataclass
from enum import Enum


class Direction(str, Enum):
    STRAIGHT = 1
    LEFT = 2
    RIGHT = 3
    
class MoveState(str, Enum):
    STOP = 0
    MOVE = 1

@dataclass
class Car():
    id: int
    type: str
    direction: "Direction"