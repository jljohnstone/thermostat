#!/usr/bin/env python3
# import json
from request_handler import RequestHandler

address = "app.gogriddy.com"
path = "/api/v1/insights/getnow"

class Griddy:

    def __init__(self, config):
        self.config = config
        self.handler = RequestHandler(address)
        self.handler.set_ssl(True)
        self.data = None

    def query(self):
        json = {
            "meterid": self.config["meter_id"],
            "memberid": self.config["member_id"],
            "settlement_point": self.config["settlement_point"]
        }
        self.data = self.handler.json_request(path, json)

    def get_current_status(self):
        # current_status = {
        #     "date": "2019-08-02T06:20:12Z",
        #     "hour_num": "6",
        #     "min_num": "20",
        #     "settlement_point": "LZ_NORTH",
        #     "price_type": "lmp",
        #     "price_ckwh": "1.48300000",
        #     "value_score": "13",
        #     "mean_price_ckwh": "4.303125",
        #     "diff_mean_ckwh": "-2.820125",
        #     "high_ckwh": "36.200000",
        #     "low_ckwh": "1.100000",
        #     "std_dev_ckwh": "5.471677",
        #     "price_display": "1.5",
        #     "price_display_sign": "¢",
        #     "date_local_tz": "2019-08-02T01:20:12-05:00"
        # }
        # return current_status;
        return self.data["now"]