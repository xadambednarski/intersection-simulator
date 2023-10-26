import logging
import random
from datetime import datetime

from car import Direction
from constants import RANDOM_SEED
from intersection import Intersection
from traffic_lights import State, TrafficLight


def setup():
    lights = [
        TrafficLight(State.GREEN, "NS", [Direction.STRAIGHT, Direction.RIGHT]),
        TrafficLight(State.GREEN, "SN", [Direction.STRAIGHT, Direction.RIGHT]),
        TrafficLight(State.RED, "WE", [Direction.STRAIGHT, Direction.RIGHT]),
        TrafficLight(State.RED, "EW", [Direction.STRAIGHT, Direction.RIGHT]),
        TrafficLight(State.RED, "SW", [Direction.LEFT]),
        TrafficLight(State.RED, "WN", [Direction.LEFT]),
        TrafficLight(State.RED, "NE", [Direction.LEFT]),
        TrafficLight(State.RED, "ES", [Direction.LEFT]),
    ]
    intersection = Intersection(RANDOM_SEED, lights)
    logging.info("Intersection simulation started")
    intersection.run()

    logging.info("Intersection simulation finished - sim time:%d", intersection.run_time)
    for light in lights:
        logging.info("Cars passed on %s: %d", light.lane, light.total_cars)
        logging.info("Longest queue on %s: %d", light.lane, light.longest_queue)
    logging.info("Total cars on intersection: %s", intersection.car_count)

random.seed(RANDOM_SEED)
setup()
