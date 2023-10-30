import logging
import random
from car import Car
from traffic_lights import State
import numpy as np


logging.basicConfig(format="%(message)s", filename="logs.log", level=logging.DEBUG)

class Intersection:
    def __init__(
        self,
        CAR_FLOW: dict,
        GREEN_LIGHTS: dict,
        INTERGREEN: list,
        YELLOW_PROB: float,
        SIM_TIME: int,
        lights: list,
    ):
        self.lights = lights
        self.sim_time = SIM_TIME
        self.yellow_prob = YELLOW_PROB
        self.intergreen = INTERGREEN
        self.green_lights = GREEN_LIGHTS
        self.car_flow = CAR_FLOW
        self.total_car_count = 0
        self.run_time = 0
        self.phase_time = 0
        self.total_phase_num = 0
        self.total_cycle_num = 0
        self.cycle = self.create_cycle()
        self.current_phase = self.cycle[0]
        self.cycle_flow = {}

    def run(self):
        phase_index = 0
        while self.sim_time > self.run_time:
            self.spawn_car()
            if self.phase_time < self.current_phase[1] - 1:
                self.phase_time += 1
            else:
                self.total_phase_num += 1
                try:
                    phase_index += 1
                    self.current_phase = self.cycle[phase_index]
                    logging.info("Phase %d -> Phase %d", phase_index-1, phase_index)
                except Exception:
                    logging.info("Phase %d -> Phase 0", phase_index)
                    for index, light in enumerate(self.lights):
                        try:
                            cc = light.cycle_car_count[self.total_cycle_num]
                            logging.info("Cars passed on lane %s during %d cycle: %d", light.lane, self.total_cycle_num, cc)
                        except:
                            continue
                    phase_index = 0
                    self.current_phase = self.cycle[phase_index]
                    self.total_cycle_num += 1
                self.phase_time = 0
            for index, light in enumerate(self.lights):
                light.check_longest_queue()
                if self.current_phase[0][index] == State.GREEN:
                    if light.queue.qsize() > 0:
                        num_cars = 1
                    else:
                        num_cars = 2
                    light.move_cars(num_cars, self.total_cycle_num)
                elif (self.current_phase[0][index] == State.YELLOW or self.current_phase[0][index] == State.RED_YELLOW) and light.queue.qsize == 0:
                    if self.draw_yellow_light_move(light.lane):
                        light.move_cars(1, self.total_cycle_num)
            self.run_time += 1

    def spawn_car(self):
        for lane in self.car_flow:
            spawn_prob = self.car_flow[lane] / 3600
            # is_spawned = bool(np.random.choice([0, 1], p=[1 - spawn_prob, spawn_prob]))
            if spawn_prob > random.random():
                light = next((x for x in self.lights if x.lane == lane), None)
                car = Car(self.total_car_count)
                light.queue.put(car)
                self.total_car_count += 1

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
            0: [phase_0, self.green_lights[0]],
            1: [phase_0_to_1, self.intergreen[0]],
            2: [phase_0_to_1_2, self.intergreen[1]],
            3: [phase_1, self.green_lights[1]],
            4: [phase_1_to_2, self.intergreen[0]],
            5: [phase_1_to_2_2, self.intergreen[1]],
            6: [phase_2, self.green_lights[2]],
            7: [phase_2_to_3, self.intergreen[0]],
            8: [phase_2_to_3_2, self.intergreen[1]],
            9: [phase_3, self.green_lights[3]],
            10: [phase_3_to_0, self.intergreen[0]],
            11: [phase_3_to_0_2, self.intergreen[1]],
        }

    def draw_yellow_light_move(self, lane:str) -> bool:
        # is_allowed = bool(np.random.choice([0, 1], p=[1 - self.yellow_prob, self.yellow_prob]))
        if self.yellow_prob > random.random():
            print("x")
            logging.info("Car passed on lane %s on yellow light", lane)
            return True
        return False
