from enum import Enum
from queue import Queue

class State(Enum):
    RED = 1
    YELLOW = 2
    RED_YELLOW = 3
    GREEN = 4


class TrafficLight:
    def __init__(self, state: State, lane: str, directions: list):
        self.lane = lane
        self.state = state
        self.directions = directions
        self.queue = Queue()
        self.total_cars = 0
        self.cycle_car_count = {}
        self.longest_queue = 0

    def move_cars(self, num: int, cycle: int) -> int:
        for _ in range(num):
            if self.queue.qsize() > 0:
                car = self.queue.get()
                self.total_cars += 1
                try:
                    self.cycle_car_count[cycle] += 1
                except:
                    self.cycle_car_count[cycle] = 1

    def check_longest_queue(self):
        if self.queue.qsize() > self.longest_queue:
            self.longest_queue = self.queue.qsize()

    def get_avg_car_flow(self, cycles_num):
        return self.total_cars / cycles_num
