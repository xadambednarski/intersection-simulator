from enum import Enum
from queue import Queue
from .vehicle import Direction
from collections import defaultdict


class State(Enum):
    """Enumerating traffic lights signals"""

    RED = 3
    YELLOW = 2
    RED_YELLOW = 4
    GREEN = 1


class TrafficLight:
    """Class of traffic lights objects which is gathering statistical data for its every object"""

    def __init__(self, state: State, lanes: list, queue: Queue):
        self.lanes = lanes
        self.state = state
        self.queue = queue
        self.cycle_vehicle_count = defaultdict(dict)
        self.longest_queue = 0

    def check_direction(self):
        """Mapping lanes to directions of vehicles turns"""
        lane_to_direction = {
            "NS": Direction.STRAIGHT,
            "SN": Direction.STRAIGHT,
            "WE": Direction.STRAIGHT,
            "EW": Direction.STRAIGHT,
            "NW": Direction.RIGHT,
            "SE": Direction.RIGHT,
            "WS": Direction.RIGHT,
            "EN": Direction.RIGHT,
            "SW": Direction.LEFT,
            "WN": Direction.LEFT,
            "NE": Direction.LEFT,
            "ES": Direction.LEFT,
        }
        return lane_to_direction

    def check_longest_queue(self):
        """Updating longest queue value created before traffic lights if it's needed"""
        if self.queue.qsize() > self.longest_queue:
            self.longest_queue = self.queue.qsize()

    def get_avg_vehicles_flow(self, lane, cycles_num):
        """Updating average vehicles flow on every lane serving by traffic lights"""
        sum = 0
        for cycle in self.cycle_vehicle_count:
            try:
                sum += self.cycle_vehicle_count[cycle][lane]
            except:
                continue
        return sum / cycles_num
