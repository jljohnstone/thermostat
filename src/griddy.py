#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# griddy.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from request_handler import RequestHandler


address = "app.gogriddy.com"
path = "/api/v1/insights/getnow"


class Griddy:

    def __init__(self, meter_id, member_id, settlement_point):
        self.meter_id = meter_id
        self.member_id = member_id
        self.settlement_point = settlement_point
        self.handler = RequestHandler(address)
        self.handler.set_ssl(True)
        self.data = None

    def query(self):
        json = {
            "meterid": self.meter_id,
            "memberid": self.member_id,
            "settlement_point": self.settlement_point
        }
        self.data = self.handler.json_request(path, json)

    def get_current_status(self):
        return self.data["now"]
