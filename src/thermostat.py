#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# thermostat.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from request_handler import RequestHandler


class Thermostat:

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def get_handler(self):
        handler = RequestHandler()
        handler.set_server(self.ip_address)
        handler.use_ssl = False
        return handler

    def query_info(self):
        handler = self.get_handler()
        handler.set_path("query/info")
        return handler.send_request()

    def query_sensors(self):
        handler = self.get_handler()
        handler.set_path("query/info")
        return handler.send_request()

    def query_alerts(self):
        handler = self.get_handler()
        handler.set_path("query/alerts")
        return handler.send_request()

    def query_runtimes(self):
        handler = self.get_handler()
        handler.set_path("query/runtimes")
        return handler.send_request()

    def set_cool_temp(self, cool_temp):
        handler = self.get_handler()
        data = {"cooltemp": cool_temp}
        handler.set_path("control")
        handler.set_data(data)
        return handler.send_request("POST")
