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

    def query(self):
        json = {
            "meterid": self.config["meter_id"],
            "memberid": self.config["member_id"],
            "settlement_point": self.config["settlement_point"]
        }
        return self.handler.json_request(path, json)

