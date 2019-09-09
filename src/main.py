#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from multiprocessing import Process
from thermostat import Thermostat
import env_loader
import griddy
import log_manager
import time
import sqlite3

conn = sqlite3.connect('thermostat.db')
db = conn.cursor()
db.execute("SELECT poll_frequency FROM configuration;")
row = db.fetchone()

POLL_FREQUENCY = row[0]
ENV_FILE = "./.env.local"


config = env_loader.load_config(ENV_FILE)
log = log_manager.setup_logging(__name__)


def main(t, g):
    while True:
        griddy_data = g.query()
        current_price = griddy_data["now"]["price_ckwh"]
        price_display = g.format_price(current_price)

        if g.price_is_high(current_price):
            t.set_spike_active(True)
            log.info("Spike active. Current price: {}".format(price_display))
        else:
            t.set_spike_active(False)

        t.run()

        time.sleep(POLL_FREQUENCY)


if __name__ == "__main__":
    log.info("Thermostat monitor started.")

    t = Thermostat(config["thermostat"]["address"])

    g = griddy.Griddy(
        config["griddy"]["meter_id"],
        config["griddy"]["member_id"],
        config["griddy"]["settlement_point"]
    )

    m = Process(target = main, args=(t, g))
    m.start()
    m.join()
