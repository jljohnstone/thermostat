#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from multiprocessing import Process
from thermostat import Thermostat
import datetime
import env_loader
import griddy
import logging
import time


POLL_FREQUENCY = 150
COOL_TEMP = 79
HEAT_TEMP = 62
MAX_CENTS_PER_KWH = 5.0

config = env_loader.load_config()
t = Thermostat(config["thermostat"])
g = griddy.Griddy(config["griddy"])


def write_log(log_data):
    print(log_data)

    timestamp = str(datetime.datetime.now())
    log_line = "{} - {}".format(timestamp, log_data)

    logging.basicConfig(filename='./thermostat.log',level=logging.DEBUG)
    logging.info(log_line)


def price_is_high(current_price):
    return float(current_price) > float(MAX_CENTS_PER_KWH)


def main():

    write_log("Thermostat monitor started.")

    spike = False

    while True:
        g.query()
        griddy_data = g.get_current_status()
        current_price = griddy_data["price_ckwh"]

        thermo_data = t.query_states()
        space_temp = thermo_data["spacetemp"]
        
        # Price is high, so check if thermostat needs to be adjusted.
        if price_is_high(current_price):

            spike = True

            # Venstar API: 2 = cooling state
            if thermo_data["state"] == 2:
                t.set_cool_temp(space_temp + 2)

                write_log(
                    "Spike detected. [space temp: {}, cool temp: {}, current price: {}]".format(
                        space_temp,
                        thermo_data["cooltemp"],
                        current_price
                    )
                )

                new_cool_temp = space_temp + 2

                write_log("Setting cool temp to {}".format(new_cool_temp))

                t.set_cool_temp(new_cool_temp)

        else:

            # Price is not high, so maintain current temperature programming.
            t.set_cool_temp(COOL_TEMP)

            # Unflag an existing spike.
            if spike is True:

                spike = False

                write_log(
                    "Spike ended. [space temp: {}, cool temp: {}, current price: {}]".format(
                        space_temp,
                        thermo_data["cooltemp"],
                        current_price
                    )
                )

                write_log("Resuming program; cool temp set to {}".format(COOL_TEMP))

        time.sleep(POLL_FREQUENCY)


if __name__ == "__main__":
    p = Process(target = main)
    p.start()
    p.join()
