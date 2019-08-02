#!/usr/bin/env python3

from thermostat import Thermostat
import env_loader
import griddy


config = env_loader.load_config()


# g = griddy.Griddy(config["griddy"])
# costs = g.query()
# print(costs)

thermo = Thermostat(config["thermostat"])

# states = thermo.query_states()
# # sensors = thermo.query_sensors()

# print(states)
# print(sensors)

# data = response(url)
# print(json.loads(data))
