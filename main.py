import random
from traffic_lights import TrafficLight, State
from intersection import Intersection
import logging
from datetime import datetime
from car import Direction 
from constants import RANDOM_SEED, SIM_TIME

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)


def setup():
    light_ns = TrafficLight(State.GREEN, "NS", [Direction.STRAIGHT, Direction.RIGHT])
    light_sn = TrafficLight(State.GREEN, "SN", [Direction.STRAIGHT, Direction.RIGHT])
    light_we = TrafficLight(State.RED, "WE", [Direction.STRAIGHT, Direction.RIGHT])
    light_ew = TrafficLight(State.RED, "EW", [Direction.STRAIGHT, Direction.RIGHT])
    light_sw = TrafficLight(State.RED, "SW", [Direction.LEFT])
    light_wn = TrafficLight(State.RED, "WN", [Direction.LEFT])
    light_ne = TrafficLight(State.RED, "NE", [Direction.LEFT])
    light_es = TrafficLight(State.RED, "ES", [Direction.LEFT])
    lights = [light_ns, light_sn, light_we, light_ew, light_wn, light_es, light_sw, light_ne]
    intersection = Intersection(RANDOM_SEED, lights)
    now = datetime.now().strftime("%d.%m.%Y %H:%m:%S")
    logging.info("%s - Intersection simulation started", now)
    intersection.run()
    
    now = datetime.now().strftime("%d.%m.%Y %H:%m:%S")
    logging.info("%s - Intersection simulation ended", now)
    for light in lights:
        logging.info("Cars passed on %s: %d", light.lane, light.total_cars)


random.seed(RANDOM_SEED)
setup()
