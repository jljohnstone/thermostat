#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from multiprocessing import Process
from thermostat import Thermostat
import datetime
import env_loader
import griddy
import logger
import time
import sys

POLL_PROVIDER_FREQUENCY = 150
COOL_TEMP = 78
HEAT_TEMP = 62
MAX_CENTS_PER_KWH = 5.0
ENV_FILE = "./.env.local"


config = env_loader.load_config(ENV_FILE)
t = Thermostat(config["thermostat"]["address"])
g = griddy.Griddy(
    config["griddy"]["meter_id"],
    config["griddy"]["member_id"],
    config["griddy"]["settlement_point"]
)


def price_is_high(current_price):
    return float(current_price) > float(MAX_CENTS_PER_KWH)


def state_logger():
    is_active = False

    while True:
        info = t.query_info()
        is_active = logger.log_thermostat_state(info["state"], is_active)
        time.sleep(60)


def spike_handler(thermo_data, current_price, spike_status):
    thermostat_state = thermo_data["state"] 
    space_temp = thermo_data["spacetemp"]
    temp_delta = 2
    cool_temp = thermo_data["cooltemp"]

    # Price is high, so check if thermostat needs to be adjusted.
    if price_is_high(current_price):

        # Venstar API: 2 = cooling state
        if thermostat_state == 2:

            logger.write_log(
                "Spike detected. [space temp: {}, cool temp: {}, current price: {}]".format(
                    space_temp,
                    cool_temp,
                    current_price
                )
            )

            new_cool_temp = space_temp + temp_delta
            t.set_cool_temp(new_cool_temp)
            logger.write_log("Setting cool temp to {}".format(new_cool_temp))

            return True

    else:

        # Price is not high, so maintain current temperature programming.
        t.set_cool_temp(COOL_TEMP)

        # Unflag an existing spike.
        if spike_status is True:

            logger.write_log(
                "Spike ended. [space temp: {}, cool temp: {}, current price: {}]".format(
                    space_temp,
                    cool_temp,
                    current_price
                )
            )

            logger.write_log("Resuming program; cool temp set to {}".format(COOL_TEMP))

            return False


def main():
    logger.write_log("Thermostat monitor started.")

    spike_status = False

    while True:
        g.query()
        current_price = g.get_current_price()
        
        thermo_data = t.query_info()
        
        spike_status = spike_handler(thermo_data, current_price, spike_status)

        time.sleep(POLL_PROVIDER_FREQUENCY)


if __name__ == "__main__":
    m = Process(target = main)
    s = Process(target = state_logger)
    m.start()
    s.start()
    m.join()
    s.join()
