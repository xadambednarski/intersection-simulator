import random
from traffic_lights import TrafficLights, State
from intersection import Intersection
import logging
from datetime import datetime
from car import Direction 
from constants import RANDOM_SEED, SIM_TIME, LIGHTS_TIMES

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)


def setup():
    light_ns = TrafficLights(State.GREEN, "NS", [Direction.STRAIGHT, Direction.RIGHT], LIGHTS_TIMES[1])
    light_sn = TrafficLights(State.GREEN, "SN", [Direction.STRAIGHT, Direction.RIGHT], LIGHTS_TIMES[1])
    light_we = TrafficLights(State.RED, "WE", [Direction.STRAIGHT, Direction.RIGHT], LIGHTS_TIMES[2])
    light_ew = TrafficLights(State.RED, "EW", [Direction.STRAIGHT, Direction.RIGHT], LIGHTS_TIMES[2])
    light_sw = TrafficLights(State.RED, "SW", [Direction.LEFT], LIGHTS_TIMES[4])
    light_wn = TrafficLights(State.RED, "WN", [Direction.LEFT], LIGHTS_TIMES[3])
    light_ne = TrafficLights(State.RED, "NE", [Direction.LEFT], LIGHTS_TIMES[4])
    light_es = TrafficLights(State.RED, "ES", [Direction.LEFT], LIGHTS_TIMES[3])
    lights = {1: [light_sn, light_ns], 2: [light_ew, light_we], 3: [light_wn, light_es], 4: [light_sw, light_ne]}
    intersection = Intersection(SIM_TIME, RANDOM_SEED, lights)
    now = datetime.now().strftime("%d.%m.%Y %H:%m:%S")
    logging.info("%s - Intersection simulation started", now)
    intersection.run()
    
    now = datetime.now().strftime("%d.%m.%Y %H:%m:%S")
    logging.info("%s - Intersection simulation ended", now)
    for light_pair in lights.values():
        logging.info("Cars passed on %s: %d", light_pair[0].lane, light_pair[0].total_cars)
        logging.info("Cars passed on %s: %d", light_pair[1].lane, light_pair[1].total_cars)


random.seed(RANDOM_SEED)
setup()
