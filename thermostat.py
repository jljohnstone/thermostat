#!/usr/bin/env python3
from request_handler import RequestHandler

class Thermostat:

    def __init__(self, config):
        self.config = config
        self.handler = RequestHandler(config["address"])

    # Call this method to use HTTPS on the endpoint.
    def use_ssl(self):
        self.handler.set_ssl(True)

    def query_states(self):
        path = "query/info"
        return self.handler.request(path)

    def query_sensors(self):
        path = "query/sensors"
        return self.handler.request(path)

    def query_alerts(self):
        path = "query/alerts"
        return self.handler.request(path)

    def query_runtimes(self):
        path = "query/runtimes"
        return self.handler.request(path)

    def set_cool_temp(self, cool_temp):
        path = "control"
        method = "POST"
        data = {"cooltemp": cool_temp}
        return self.handler.request(path, method, data)
