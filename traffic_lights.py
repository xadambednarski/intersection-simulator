from constants import LIGHTS_TIMES
from enum import Enum
from queue import Queue
from car import Direction
import logging
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)


class State(Enum):
    RED = 1
    YELLOW = 2
    RED_YELLOW = 3
    GREEN = 4

class TrafficLights():
    def __init__(self, state, lane, directions, lights_cycle):
        self.lane = lane
        self.state = state
        self.lights_cycle = lights_cycle
        self.time_left = get_time_left()
        self.queue = Queue()
        self.total_cars = 0
        self.directions = directions

    def change_state(self):
        if self.state == State.RED:
            self.state = State.RED_YELLOW
            self.time_left = self.lights_cycle[str(self.state.name)]
        elif self.state == State.RED_YELLOW:
            self.state = State.GREEN
            self.time_left = self.lights_cycle[str(self.state.name)]
        elif self.state == State.GREEN:
            self.state = State.YELLOW
            self.time_left = self.lights_cycle[str(self.state.name)]
        elif self.state == State.YELLOW:
            self.state = State.RED
            sum_red = 0
            for lights_cycle in LIGHTS_TIMES.values():
                sum_red += lights_cycle["RED"]
            sum_red -= self.lights_cycle[str(self.state.name)]
            self.time_left = sum_red

    def get_time_left(self):
        if self.state == State.YELLOW:
            sum_red = 0
            for lights_cycle in LIGHTS_TIMES.values():
                sum_red += lights_cycle["RED"]
            sum_red -= self.lights_cycle[str(self.state.name)]
            self.time_left = sum_red
    def move_cars(self):
        if self.queue.qsize() > 0:
            car = self.queue.get()
            self.total_cars += 1