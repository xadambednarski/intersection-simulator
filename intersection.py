import logging
from car import Car, Direction
import random
from traffic_lights import State
import numpy as np
from utils import pairwise
from constants import SIM_TIME, CAR_FLOW, GREEN_LIGHTS, CYCLE_TIME
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)


class Intersection():
    def __init__(self, seed, lights):
        self.lights = lights
        self.seed = seed
        self.car_count = 0
        self.run_time = 0
        self.cycle = self.create_cycle()
        self.current_phase = self.cycle[0]
        self.phase_time = 0

    def run(self):
        phase_index = 0
        while SIM_TIME > self.run_time:
            if self.phase_time < self.current_phase[1]:
                self.phase_time += 1
            else:
                print("changing phase, current: ", self.current_phase)
                try:
                    phase_index += 1
                    self.current_phase = self.cycle[phase_index]
                except:
                    phase_index = 0
                    self.current_phase = self.cycle[phase_index]
                self.phase_time = 0
                print("new phase:", self.current_phase)
            # self.spawn_car()
            self.run_time += 1

    def spawn_car(self):
        for lane in CAR_FLOW:
            spawn_prob = CAR_FLOW[lane] / 3600
            is_spawned = bool(np.random.choice([0, 1], p=[1-spawn_prob, spawn_prob]))
            if is_spawned:
                light = next((x for x in self.lights if x.lane == lane), None)
                car = Car(self.car_count, "car", light.direction)
                light.queue.put(car)
                self.car_count += 1

    def create_cycle(self):
        phase_0 = [State.GREEN, State.GREEN] + [State.RED for _ in range(len(self.lights) - 2)]
        phase_1 = [State.RED, State.RED, State.GREEN, State.GREEN] + [State.RED for _ in range(len(self.lights) - 4)]
        phase_2 = [State.RED for _ in range(len(self.lights) - 4)] + [State.GREEN, State.GREEN, State.RED, State.RED]
        phase_3 = [State.RED for _ in range(len(self.lights) - 2)] + [State.GREEN, State.GREEN]
        return {0: [phase_0, GREEN_LIGHTS[0]], 1: [phase_1, GREEN_LIGHTS[1]], 2: [phase_2, GREEN_LIGHTS[2]], 3: [phase_3, GREEN_LIGHTS[3]]}
