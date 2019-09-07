#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# griddy.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from request_handler import RequestHandler
import log_manager


class Griddy:

    SERVER = "app.gogriddy.com"
    PATH = "/api/v1/insights/getnow"
    MAX_CENTS_PER_KWH = 5.0

    def __init__(self, meter_id, member_id, settlement_point):
        self.meter_id = meter_id
        self.member_id = member_id
        self.settlement_point = settlement_point
        self.price = None
        self.logger = log_manager.setup_logging(__name__)

    def query(self):
        json_data = {
            "meterid": self.meter_id,
            "memberid": self.member_id,
            "settlement_point": self.settlement_point
        }

        data = (
            RequestHandler()
            .set_server(self.SERVER)
            .set_path(self.PATH)
            .set_data(json_data)
            .send_request()
        )

        self.compare_price(data["now"]["price_ckwh"])

        return data

    def price_is_high(self, current_price):
        return float(current_price) > float(self.MAX_CENTS_PER_KWH)

    def compare_price(self, current_price):
        if self.price != current_price:
            if not self.price:
                self.logger.info(
                    "Initialized price: {}".format(self.format_price(current_price))
                )
            else:
                self.logger.info(
                    "Price changed: {} --> {}".format(
                        self.format_price(self.price), self.format_price(current_price)
                    )
                )
            self.price = current_price

    def format_price(self, price):
        return "{0:.6f}".format(float(price))

