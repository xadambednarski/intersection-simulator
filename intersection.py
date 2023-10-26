import logging

import numpy as np
import random
from car import Car, Direction
from constants import (CAR_FLOW, GREEN_LIGHTS, INTERGREEN, RIGHT_TURN_PROB,
                       SIM_TIME, YELLOW_PROB)
from traffic_lights import State

logging.basicConfig(filename="sim_run.log", encoding="utf-8", level=logging.DEBUG)


class Intersection:
    def __init__(self, seed: int, lights: list):
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
            self.spawn_car()
            if self.phase_time < self.current_phase[1] - 1:
                self.phase_time += 1
            else:
                try:
                    phase_index += 1
                    self.current_phase = self.cycle[phase_index]
                    # logging.info("Phase %i -> Phase %i", phase_index-1, phase_index)
                except Exception:
                    # logging.info("Phase %i -> Phase 0", phase_index)
                    phase_index = 0
                    self.current_phase = self.cycle[phase_index]
                self.phase_time = 0
            for index, light in enumerate(self.lights):
                light.check_longest_queue()
                if self.current_phase[0][index] == State.GREEN:
                    if light.queue.qsize() > 0:
                        num_cars = 1
                    else:
                        num_cars = 2
                    light.move_cars(num_cars)
                elif (
                    self.current_phase[0][index] == State.YELLOW
                    or self.current_phase[0][index] == State.RED_YELLOW
                ):
                    if light.queue.qsize() == 0:
                        if self.draw_yellow_light_move():
                            light.move_cars(num=1)
            self.run_time += 1

    def spawn_car(self):
        for lane in CAR_FLOW:
            spawn_prob = CAR_FLOW[lane] / 3600
            # is_spawned = bool(np.random.choice([0, 1], p=[1 - spawn_prob, spawn_prob]))
            if spawn_prob > random.random():
                light = next((x for x in self.lights if x.lane == lane), None)
                direction_prob = np.random.rand()
                if direction_prob >= RIGHT_TURN_PROB:
                    direction = Direction.RIGHT
                else:
                    direction = Direction.STRAIGHT
                car = Car(self.car_count, "car", direction)
                light.queue.put(car)
                self.car_count += 1

    def create_cycle(self) -> dict:
        phase_0 = [State.GREEN, State.GREEN] + [
            State.RED for _ in range(len(self.lights) - 2)
        ]
        phase_0_to_1 = [State.YELLOW, State.YELLOW] + [
            State.RED for _ in range(len(self.lights) - 2)
        ]
        phase_0_to_1_2 = [
            State.YELLOW,
            State.YELLOW,
            State.RED_YELLOW,
            State.RED_YELLOW,
        ] + [State.RED for _ in range(len(self.lights) - 4)]
        phase_1 = [State.RED, State.RED, State.GREEN, State.GREEN] + [
            State.RED for _ in range(len(self.lights) - 4)
        ]
        phase_1_to_2 = [State.RED, State.RED, State.YELLOW, State.YELLOW] + [
            State.RED for _ in range(len(self.lights) - 4)
        ]
        phase_1_to_2_2 = [
            State.RED,
            State.RED,
            State.YELLOW,
            State.YELLOW,
            State.RED_YELLOW,
            State.RED_YELLOW,
            State.RED,
            State.RED,
        ]
        phase_2 = [State.RED for _ in range(len(self.lights) - 4)] + [
            State.GREEN,
            State.GREEN,
            State.RED,
            State.RED,
        ]
        phase_2_to_3 = [State.RED for _ in range(len(self.lights) - 4)] + [
            State.YELLOW,
            State.YELLOW,
            State.RED,
            State.RED,
        ]
        phase_2_to_3_2 = [State.RED for _ in range(len(self.lights) - 4)] + [
            State.YELLOW,
            State.YELLOW,
            State.RED_YELLOW,
            State.RED_YELLOW,
        ]
        phase_3 = [State.RED for _ in range(len(self.lights) - 2)] + [
            State.GREEN,
            State.GREEN,
        ]
        phase_3_to_0 = [State.RED for _ in range(len(self.lights) - 2)] + [
            State.YELLOW,
            State.YELLOW,
        ]
        phase_3_to_0_2 = (
            [State.RED_YELLOW, State.RED_YELLOW]
            + [State.RED for _ in range(len(self.lights) - 4)]
            + [State.YELLOW, State.YELLOW]
        )
        return {
            0: [phase_0, GREEN_LIGHTS[0]],
            1: [phase_0_to_1, INTERGREEN[0]],
            2: [phase_0_to_1_2, INTERGREEN[1]],
            3: [phase_1, GREEN_LIGHTS[1]],
            4: [phase_1_to_2, INTERGREEN[0]],
            5: [phase_1_to_2_2, INTERGREEN[1]],
            6: [phase_2, GREEN_LIGHTS[2]],
            7: [phase_2_to_3, INTERGREEN[0]],
            8: [phase_2_to_3_2, INTERGREEN[1]],
            9: [phase_3, GREEN_LIGHTS[3]],
            10: [phase_3_to_0, INTERGREEN[0]],
            11: [phase_3_to_0_2, INTERGREEN[1]],
        }

    def draw_yellow_light_move(self) -> bool:
        is_allowed = bool(np.random.choice([0, 1], p=[1 - YELLOW_PROB, YELLOW_PROB]))
        return is_allowed
