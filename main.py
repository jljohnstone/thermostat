#!/usr/bin/env python3

from thermostat import Thermostat
import griddy
import json
import os
import sys


def load_config():
    thermostat_address = None
    griddy_meter_id = None
    griddy_member_id = None
    griddy_settlement_point = None

    try:
        blargh = os.environ["FAIL"]
        thermostat_address = os.environ["THERMOSTAT_ADDRESS"]
        griddy_meter_id = os.environ["GRIDDY_METER_ID"]
        griddy_member_id = os.environ["GRIDDY_MEMBER_ID"]
        griddy_settlement_point = os.environ["GRIDDY_SETTLEMENT_POINT"]

    except:
        print("ENVs not set. Attempting to load from dotenv file.")

        try:
            with open("./.env", "r") as f:
                lines = f.readlines()

            lines = [x.strip().split('=') for x in lines if '=' in x]

            for line in lines:
                if line[0] == "THERMOSTAT_ADDRESS":
                    thermostat_address = line[1]

                if line[0] == "GRIDDY_METER_ID":
                    griddy_meter_id = line[1]

                if line[0] == "GRIDDY_MEMBER_ID":
                    griddy_member_id = line[1]

                if line[0] == "GRIDDY_SETTLEMENT_POINT":
                    griddy_settlement_point = line[1]
            
        except:
            print("Failed to load environment variables. Exiting")
            sys.exit(1)

    config = {
        "thermostat": {
            "address": thermostat_address
        },
        "griddy": {
            "meter_id": griddy_meter_id,
            "member_id": griddy_member_id,
            "settlement_point": griddy_settlement_point
        }
    }

    return config


config = load_config()

print(config)

# g = griddy.Griddy(config["griddy"])
# costs = g.query()
# print(costs)

# thermo = Thermostat(config["thermostat"])

# states = thermo.query_states()
# # sensors = thermo.query_sensors()

# print(states)
# print(sensors)

# data = response(url)
# print(json.loads(data))
