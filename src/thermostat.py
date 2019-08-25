#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# thermostat.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from request_handler import RequestHandler


class Thermostat:

    def __init__(self, ip_address):
        self.ip_address = ip_address

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

    def query_sensors(self):
        return (
            self.get_handler()
            .set_path("query/sensors")
            .send_request()
        )

    def query_alerts(self):
        return (
            self.get_handler()
            .set_path("query/alerts")
            .send_request()
        )

    def query_runtimes(self):
        return (
            self.get_handler()
            .set_path("query/runtimes")
            .send_request()
        )

    def set_cool_temp(self, cool_temp):
        data = {"cooltemp": cool_temp}
        return (
            self.get_handler()
            .set_path("control")
            .set_data(data)
            .send_request("POST")
        )
