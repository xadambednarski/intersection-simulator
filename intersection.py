import logging
from car import Car, Direction
import random
from traffic_lights import State
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)


class Intersection():
    def __init__(self, sim_time, seed, lights):
        self.lights = lights
        self.seed = seed
        self.sim_time = sim_time
        self.car_count = 0
        self.run_time = 0
        
    def run(self):
        while self.sim_time > self.run_time:
            self.spawn_car()
            for light_pair in self.lights.values():
                logging.info(f"{light_pair[0].lane} - {light_pair[0].state}, {light_pair[0].time_left}")
                logging.info(f"{light_pair[1].lane} - {light_pair[1].state}, {light_pair[1].time_left}")
                if light_pair[0].time_left == 0:
                    light_pair[0].change_state()
                    light_pair[1].change_state()
                if light_pair[0].state.GREEN:
                    light_pair[0].move_cars()
                    light_pair[1].move_cars()
                light_pair[0].time_left -= 1
                light_pair[1].time_left -= 1
            self.run_time += 1
            
    def spawn_car(self):
        self.car_count += 1
        light = random.choice(list(self.lights.values()))[random.randint(0, 1)]
        car = Car(self.car_count, "car", random.choice(light.directions))
        light.queue.put(car)
        
       
        
            
        