#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# logger.py
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import logging
import logging.handlers


def setup_logging(logger_name):

    log_file = "./var/log/thermostat.log"

    log = logging.getLogger(logger_name)
    log.setLevel(logging.INFO)

    handler = logging.handlers.TimedRotatingFileHandler(
        log_file, 
        when="D", 
        interval=1, 
        backupCount=60
    )
    ts_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] (%(name)s): %(message)s", ts_format)

    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log

