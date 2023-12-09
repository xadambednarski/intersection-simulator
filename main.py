import logging
import datetime as dt
import json
from objects.intersection import Intersection
from queue import Queue
from objects.traffic_lights import State, TrafficLight


logging.basicConfig(format="%(message)s", filename="logs.log", level=logging.DEBUG)


def setup(conf_file: str) -> tuple:
    """Reading simulation parameters, initialilzating Traffic Lights and Intersection objects"""
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
    return (intersection, random_seed, vehicles_flow, gl, intergreen, vps, sim_time)


def log_stats(
    intersection: Intersection,
    random_seed: int,
    vehicles_num: dict,
    gl: dict,
    intergreen: list,
    vps: int,
    sim_time: int,
):
    """Formatting all gathered data and passing it to output file"""
    logging.info(
        "%s - Intersection simulation started with parameters given by"
        " user:\nSimulation time: %d\nSeed: %d\nGreen light time on"
        " lanes:\nNS/SN/SE/NW: %s\nWE/EW/EN\WS: %s\nSW/WN: %s\nNE/ES: %s\nIntergreen"
        " lights time:\nYellow: %d\nRed + Yellow: %d\nCapacity per second: %d",
        dt.datetime.now(),
        sim_time,
        random_seed,
        gl[0],
        gl[1],
        gl[2],
        gl[3],
        intergreen[0],
        intergreen[1],
        vps,
    )
    logging.info("Vehicle flow on lanes:")
    for lane in vehicles_num:
        logging.info("%s: %d", lane, vehicles_num[lane])
    logging.info("--------------------------------------------")
    logging.info(
        "%s - Intersection simulation finished - sim time: %d\n",
        dt.datetime.now(),
        intersection.run_time,
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
                "Statistics for lane %s:\nVehicles passed: %d\nLongest queue:"
                " %d\nAverage number of vehicles crossing the intersection per cycle:"
                " %f\nDesired vehicles flow per cycle: %f\n",
                lane,
                sum_cars,
                light.longest_queue,
                light.get_avg_vehicles_flow(lane, intersection.total_cycle_num),
                get_desired_vehicles_flow(
                    vehicles_num[lane], intersection.total_cycle_num
                ),
            )
    logging.info(
        "Overall intersection statistics:\nTotal number of vehicles: %d\nTotal number"
        " of cycles: %d\n",
        intersection.total_vehicle_count,
        intersection.total_cycle_num,
    )


def get_desired_vehicles_flow(vehicles_flow, cycles_num) -> float:
    """Calculating desired flow, based on number of cycles (output value) and flow of vehicles (given in parameter)"""
    return vehicles_flow / cycles_num


if __name__ == "__main__":
    try:
        intersection, seed, vehicles_flow, gl, intergreen, vps, sim_time = setup(
            "sim_parameters.json"
        )
        intersection.run()
        log_stats(intersection, seed, vehicles_flow, gl, intergreen, vps, sim_time)
    except Exception as e:
        logging.info(f"Error info: {e}\n")
        raise ValueError
