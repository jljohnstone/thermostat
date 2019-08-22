#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# request_handler.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import json
import urllib.request


class RequestHandler:

    def __init__(self):
        self.use_ssl = True
        self.server = None
        self.path = None
        self.data = None

    def set_server(self, server):
        self.server = server.strip("/ ")

    def set_path(self, path):
        trimmed_path = path.strip("/ ")

        if trimmed_path != "":
            self.path = "".join(["/", trimmed_path])

    def set_data(self, data):
        self.data = data

    def generate_url(self, path):
        if self.use_ssl:
            protocol = "https"
        else:
            protocol = "http"
        return "{}://{}{}".format(protocol, self.server, path)

    def json_decode(self, data):
        return json.loads(data)

    def send_request(self, method = "GET"):
        url = self.generate_url(self.path)
        req = urllib.request.Request(url)

        if method == "POST":
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            d = urllib.parse.urlencode(self.data).encode("utf-8")

            with urllib.request.urlopen(req, data = d) as response:
                resp = response.read()
                return resp
        else:
            req.add_header("Content-Type", "application/json")

            if self.data:
                json_data_bytes = json.dumps(self.data).encode("utf-8")
            else:
                json_data_bytes = None

            with urllib.request.urlopen(url, json_data_bytes) as response:
                return self.json_decode(response.read())
