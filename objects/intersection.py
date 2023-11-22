import logging
import random
from objects.vehicle import Vehicle
from objects.traffic_lights import State

logging.basicConfig(format="%(message)s", filename="logs.log", level=logging.DEBUG)


class Intersection:
    def __init__(
        self,
        vehicles_flow: dict,
        green_lights: dict,
        intergreen: list,
        sim_time: int,
        lights: list,
        vps: int,
        random_seed: int,
    ):
        self.lights = lights
        self.sim_time = sim_time
        self.intergreen = intergreen
        self.green_lights = green_lights
        self.vehicles_flow = vehicles_flow
        self.vps = vps
        self.random_seed = random.seed(random_seed)
        self.total_vehicle_count = 0
        self.run_time = 0
        self.phase_time = 0
        self.total_phase_num = 0
        self.phase_index = 0
        self.total_cycle_num = 0
        self.cycle = self.create_cycle()
        self.current_phase = self.cycle[0]
        self.cycle_flow = {}

    def run(self):
        while self.sim_time > self.run_time:
            self.spawn_vehicle()
            self.move_vehicles()
            self.monitor_phase()
            self.run_time += 1

    def move_vehicles(self):
        for index, light in enumerate(self.lights):
            light.check_longest_queue()
            if self.current_phase[0][index] == State.GREEN and light.queue.qsize() > 0:
                for _ in range(self.vps):
                    if light.queue.qsize() > 0:
                        vehicle = light.queue.get()
                        for key, value in light.check_direction().items():
                            if vehicle.direction == value and key in light.lanes:
                                lane_direction = key
                        try:
                            lane_direction
                            try:
                                light.cycle_vehicle_count[self.total_cycle_num][
                                    lane_direction
                                ] += 1
                            except:
                                light.cycle_vehicle_count[self.total_cycle_num][
                                    lane_direction
                                ] = 1
                        except:
                            pass

    def spawn_vehicle(self):
        for lane in self.vehicles_flow:
            spawn_prob = self.vehicles_flow[lane] / 3600
            if spawn_prob > random.random():
                light = next((x for x in self.lights if lane in x.lanes), None)
                direction = light.check_direction()[lane]
                vehicle = Vehicle(self.total_vehicle_count, direction)
                light.queue.put(vehicle)
                self.total_vehicle_count += 1

    def monitor_phase(self):
        if self.phase_time < self.current_phase[1] - 1:
            self.phase_time += 1
        else:
            self.total_phase_num += 1
            try:
                self.phase_index += 1
                self.current_phase = self.cycle[self.phase_index]
            except Exception:
                self.phase_index = 0
                self.current_phase = self.cycle[self.phase_index]
                self.total_cycle_num += 1
            self.phase_time = 0

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
            1: [phase_0_to_1, self.intergreen[0] - 1],
            2: [phase_0_to_1_2, self.intergreen[1]],
            3: [phase_1, self.green_lights[1]],
            4: [phase_1_to_2, self.intergreen[0] - 1],
            5: [phase_1_to_2_2, self.intergreen[1]],
            6: [phase_2, self.green_lights[2]],
            7: [phase_2_to_3, self.intergreen[0] - 1],
            8: [phase_2_to_3_2, self.intergreen[1]],
            9: [phase_3, self.green_lights[3]],
            10: [phase_3_to_0, self.intergreen[0] - 1],
            11: [phase_3_to_0_2, self.intergreen[1]],
        }
