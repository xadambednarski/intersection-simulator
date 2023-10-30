import logging
import random
from car import Direction
from constants import (
    RANDOM_SEED,
    CAR_FLOW,
    GREEN_LIGHTS,
    INTERGREEN,
    YELLOW_PROB,
    SIM_TIME,
)
from intersection import Intersection
from traffic_lights import State, TrafficLight

logging.basicConfig(format="%(message)s", filename="logs.log", level=logging.DEBUG)


def setup(CAR_FLOW, GREEN_LIGHTS, INTERGREEN, YELLOW_PROB):
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
    intersection = Intersection(
        CAR_FLOW, GREEN_LIGHTS, INTERGREEN, YELLOW_PROB, SIM_TIME, lights
    )
    logging.info(
        "Intersection simulation started with parameters:\nSeed: %d\nEstimated car flow: %s\nGreen light time on lanes:\nNS/SN: %s\nWE/EW: %s\nSW/WN: %s\nNE/ES: %s\nIntergreen lights time:\nYellow: %d\nRed + Yellow: %d\nProbability of crossing intersection on yellow light event: %f\n",
        RANDOM_SEED,
        CAR_FLOW,
        GREEN_LIGHTS[0],
        GREEN_LIGHTS[1],
        GREEN_LIGHTS[2],
        GREEN_LIGHTS[3],
        INTERGREEN[0],
        INTERGREEN[1],
        YELLOW_PROB,
    )
    intersection.run()

    logging.info(
        "Intersection simulation finished - sim time: %d\n", intersection.run_time
    )
    for light in lights:
        logging.info(
            "Statistics for lane %s:\nCars passed: %d\nLongest queue: %d\nAverage number of cars crossing the intersection per cycle: %f\nDesired car flow per cycle: %f\n",
            light.lane,
            light.total_cars,
            light.longest_queue,
            light.get_avg_car_flow(intersection.total_cycle_num),
            get_desired_car_flow(light, intersection.total_cycle_num),
        )
    logging.info(
        "Overall intersection statistics\nTotal number of cars: %d\nTotal number of cycles: %d",
        intersection.total_car_count,
        intersection.total_cycle_num,
    )


def get_desired_car_flow(light, cycles_num):
    return CAR_FLOW[light.lane] / cycles_num


random.seed(RANDOM_SEED)
setup(CAR_FLOW, GREEN_LIGHTS, INTERGREEN, YELLOW_PROB)
