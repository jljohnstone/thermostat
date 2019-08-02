#!/usr/bin/env python3
import json
import urllib.request

class RequestHandler:

    def __init__(self, server):
        self.server = server.strip('/ ')
        self.set_ssl(False)
    
    def set_ssl(self, is_ssl):
        if is_ssl:
            self.protocol = "https"
        else:
            self.protocol = "http"

    def generate_url(self, path):
        return "{}://{}/{}".format(self.protocol, self.server, path)

    def json_decode(self, data):
        return json.loads(data)

    def request(self, path):
        url = self.generate_url(path.strip('/ '))

        with urllib.request.urlopen(url) as response:
            return self.json_decode(response.read())

    def json_request(self, path, body):
        url = self.generate_url(path.strip('/ '))
        req = urllib.request.Request(url)
        req.add_header("Content-Type", "application/json")
        json_data = json.dumps(body)
        json_data_bytes = json_data.encode("utf-8")

        with urllib.request.urlopen(url, json_data_bytes) as response:
            return self.json_decode(response.read())