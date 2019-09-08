#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# thermostat.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Venstar API reference:
#   https://developer.venstar.com/restcalls.html


from request_handler import RequestHandler
import json
import log_manager


class Thermostat:

    COOL_TEMP = 23
    HEAT_TEMP = 19
    DEFAULT_MODE = "auto"

    MODE_MAP = {
        "off": 0,
        "heat": 1,
        "cool": 2,
        "auto": 3
    }

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.price_protected = True
        self.spike_active = False
        self.logger = log_manager.setup_logging(__name__)

    def get_handler(self):
        return (
            RequestHandler()
            .set_protocol("http")
            .set_server(self.ip_address)
        )

    def query_info(self):
        return (
            self.get_handler()
            .set_path("query/info")
            .send_request()
        )

    def is_price_protected(self):
        return self.price_protected

    def set_price_protected(self, price_protected):
        self.price_protected = price_protected

    def is_spike_active(self):
        return self.spike_active

    def set_spike_active(self, spike_active):
        self.spike_active = spike_active

    def set_cool_temp(self, cool_temp):
        data = {"cooltemp": cool_temp}
        status = (
            self.get_handler()
            .set_path("control")
            .set_data(data)
            .send_request("POST")
        )

    def set_heat_temp(self, heat_temp):
        data = {"heattemp": heat_temp}
        status = (
            self.get_handler()
            .set_path("control")
            .set_data(data)
            .send_request("POST")
        )

    # If price protection is enabled during price surges,
    # Set the thermostat mode to 'off.'
    def manage_mode(self):

        # Spike is active.
        if self.is_spike_active():

            # Price protection is enabled.
            if self.is_price_protected():
                self.logger.info(
                    "Price protection enabled; thermostat mode is 'off.'"
                )
                return self.MODE_MAP["off"]

            else:
                # Price protection is not enabled.
                self.logger.warn("Price protection is not enabled!")
                return self.MODE_MAP[self.DEFAULT_MODE]

        # Spike is not active
        else:
            return self.MODE_MAP[self.DEFAULT_MODE]


    # To-do: replace the hard-coded data settings stored in the json
    # dictionary with a database query result.
    def run(self):

        data = {}
        info = self.query_info()
        mode = self.manage_mode()

        data["mode"] = mode
        data["cooltemp"] = self.COOL_TEMP
        data["heattemp"] = self.HEAT_TEMP

        response = (
            self.get_handler()
            .set_path("control")
            .set_data(data)
            .send_request("POST")
        )

        deserialized = json.loads(response)

        if deserialized["success"]:
            self.logger.info(
                "Thermostat updated - mode {}, state {}, cool temp: {}, heat temp: {}, space temp: {}".format(
                    mode,
                    info["state"],
                    self.COOL_TEMP,
                    self.HEAT_TEMP,
                    info["spacetemp"]
                )
            )
        else:
            self.logger.error("Failed to update the thermostat.")
