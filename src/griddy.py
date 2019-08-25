#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# griddy.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from request_handler import RequestHandler


class Griddy:

    SERVER = "app.gogriddy.com"
    PATH = "/api/v1/insights/getnow"

    def __init__(self, meter_id, member_id, settlement_point):
        self.meter_id = meter_id
        self.member_id = member_id
        self.settlement_point = settlement_point
        self.data = None

    def query(self):
        json_data = {
            "meterid": self.meter_id,
            "memberid": self.member_id,
            "settlement_point": self.settlement_point
        }

        self.data = (
            RequestHandler()
            .set_server(self.SERVER)
            .set_path(self.PATH)
            .set_data(json_data)
            .send_request()
        )

    def get_current_price(self):
        return self.data["now"]["price_ckwh"]
