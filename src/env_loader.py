#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# env_loader.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
import sys


class ENVLoaderException(Exception):
    def __init__(self, message):
        self.message = "ENVLoaderException: {}".format(message)


def load_config(env_file):

    # Set a list of expected ENV keys.
    required_envs = (
        "thermostat_address",
        "griddy_meter_id",
        "griddy_member_id",
        "griddy_settlement_point"
    )

    raw_config = {}

    try:
        with open(env_file, "r") as f:
            lines = f.readlines()

        # Convert the ENV file lines to key-value entries.
        found = 0;
        lines = [x.strip().split('=') for x in lines if '=' in x]
        for line in lines:
            key = line[0].lower()
            raw_config[key] = line[1]

            # Track expected key matches.
            if key in required_envs and line[1] != "":
                found += 1

        if found != len(required_envs):
            raise ENVLoaderException("A required environment variable is missing or not set.") 

    except ENVLoaderException as e:
        print(e)
        sys.exit(1)

    except Exception:
        print("Unable to load and process the ENV file.")
        sys.exit(1)

    config = {
        "thermostat": {
            "address": raw_config["thermostat_address"]
        },
        "griddy": {
            "meter_id": raw_config["griddy_meter_id"],
            "member_id": raw_config["griddy_member_id"],
            "settlement_point": raw_config["griddy_settlement_point"]
        }
    }

    return config
