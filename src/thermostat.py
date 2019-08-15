#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# thermostat.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from request_handler import RequestHandler


class Thermostat:

    def __init__(self, ip_address):
        self.handler = RequestHandler(ip_address)

    # Call this method to use HTTPS on the endpoint.
    def use_ssl(self):
        self.handler.set_ssl(True)

    def query_info(self):
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
