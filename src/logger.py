#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# logger.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import datetime
import logging
import time


def write_log(log_data):
    print(log_data)

    timestamp = str(datetime.datetime.now())
    log_line = "{} - {}".format(timestamp, log_data)

    logging.basicConfig(filename='./thermostat.log',level=logging.DEBUG)
    logging.info(log_line)


def log_thermostat_state(thermostat_state, is_active):

    # Venstar API:
    #   0 = idle
    #   1 = heating
    #   2 = cooling
    #   3 = lockout
    #   4 = error
    if thermostat_state == 0:
        
        if is_active: 
            is_active = False
            write_log("Thermostat state set to idle.")

    elif thermostat_state == 1 or thermostat_state == 2:

        if not is_active:
            is_active = True

            if thermostat_state == 1:
                write_log("Thermostat state set to heating.")
            else:
                write_log("Thermostat state set to cooling.")

    elif thermostat_state == 3 or thermostat_state == 4:

        if thermostat_state == 3:
            write_log("Thermostat state set to lockout.")
        else:
            write_log("Thermostat state set to error.")

    return is_active
