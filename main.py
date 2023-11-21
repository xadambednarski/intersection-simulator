import logging
import random
import datetime as dt
import json
from objects.intersection import Intersection
from queue import Queue
import sys
from objects.traffic_lights import State, TrafficLight


logging.basicConfig(format="%(message)s", filename="logs.log", level=logging.DEBUG)


def setup(conf_file):
    with open(conf_file, "r") as f:
        params = json.load(f)
        vehicles_flow = params["vehicles_flow"]
        random_seed = params["random_seed"]
        sim_time = params["sim_time"]
        green_lights = params["green_lights"]
        gl = {}
        for index, lights in enumerate(green_lights):
            gl[index] = green_lights[lights]
        intergreen = params["intergreen"]
        vps = params["vps"]

    lights = [
        TrafficLight(State.GREEN, ["NS", "NW"], Queue()),
        TrafficLight(State.GREEN, ["SN", "SE"], Queue()),
        TrafficLight(State.RED, ["WE", "WS"], Queue()),
        TrafficLight(State.RED, ["EW", "EN"], Queue()),
        TrafficLight(State.RED, ["SW"], Queue()),
        TrafficLight(State.RED, ["WN"], Queue()),
        TrafficLight(State.RED, ["NE"], Queue()),
        TrafficLight(State.RED, ["ES"], Queue()),
    ]

    intersection = Intersection(
        vehicles_flow, gl, intergreen, sim_time, lights, vps, random_seed
    )
    return intersection, random_seed, vehicles_flow, gl, intergreen, vps, sim_time

def log_stats(intersection: Intersection, random_seed: int, vehicles_num: dict, gl: dict, intergreen: list, vps: int, sim_time: int):
    logging.info(
        "%s - Intersection simulation started with parameters given by user:\n\nSimulation time: %d\n\nSeed: %d\n\nGreen light time on lanes:\n\nNS/SN: %s\n\nWE/EW: %s\n\nSW/WN: %s\n\nNE/ES: %s\n\nIntergreen lights time:\n\nYellow: %d\n\nRed + Yellow: %d\n\nCapacity per second: %d\n",
        dt.datetime.now(),
        sim_time,
        random_seed,
        gl[0],
        gl[1],
        gl[2],
        gl[3],
        intergreen[0],
        intergreen[1],
        vps
    )
    for lane in vehicles_num:
        logging.info(
        "Vehicle flow on lane %s: %d\n", lane, vehicles_num[lane])

    logging.info(
        "%s - Intersection simulation finished - sim time: %d\n", dt.datetime.now(), intersection.run_time
    )
    for light in intersection.lights:
        for lane in light.lanes:
            sum_cars = 0
            for i in range(intersection.total_cycle_num):
                try:
                    sum_cars += light.cycle_vehicle_count[i][lane]
                except:
                    continue
            logging.info(
                "Statistics for lane %s:\nVehicles passed: %d\nLongest queue: %d\nAverage number of vehicles crossing the intersection per cycle: %f\nDesired vehicles flow per cycle: %f\n",
                lane,
                sum_cars,
                light.longest_queue,
                light.get_avg_vehicles_flow(lane, intersection.total_cycle_num),
                get_desired_vehicles_flow(vehicles_num[lane], intersection.total_cycle_num),
            )
    logging.info(
        "Overall intersection statistics:\nTotal number of vehicles: %d\nTotal number of cycles: %d",
        intersection.total_vehicle_count,
        intersection.total_cycle_num,
    )

def get_desired_vehicles_flow(vehicles_flow, cycles_num):
    return vehicles_flow / cycles_num


if __name__ == "__main__":
    try:
        intersection, seed, vehicles_flow, gl, intergreen, vps, sim_time = setup("sim_parameters.json")
        intersection.run()
        log_stats(intersection, seed, vehicles_flow, gl, intergreen, vps, sim_time)
    except Exception as e:
        logging.info(f"Error info: {e}")
        raise ValueError


