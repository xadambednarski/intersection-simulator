import logging
from enum import Enum
from queue import Queue

logging.basicConfig(filename="sim_run.log", encoding="utf-8", level=logging.DEBUG)


class State(Enum):
    RED = 1
    YELLOW = 2
    RED_YELLOW = 3
    GREEN = 4


class TrafficLight:
    def __init__(self, state:State, lane:str, directions:list):
        self.lane = lane
        self.state = state
        self.directions = directions
        self.queue = Queue()
        self.total_cars = 0
        self.longest_queue = 0

    def move_cars(self, num:int) -> int:
        for _ in range(num):
            if self.queue.qsize() > 0:
                car = self.queue.get()
                self.total_cars += 1

    def check_longest_queue(self):
        if self.queue.qsize() > self.longest_queue:
            self.longest_queue = self.queue.qsize()
        
