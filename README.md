# Thermostat Manager

Monitor the [Griddy](https://www.gogriddy.com/) wholesale energy provider and make thermostat adjustments during price spikes. 

## Overview

A call to the Griddy API retrieves current pricing, which is controlled and updated by [ERCOT](https://www.ercot.com/) every five minutes. The current price-per-kWh is used to change the thermostat's state and prevent or reduce consumption during peak electrical demand.

This project is designed around the Venstar series of thermostats implementing a local REST API. (See the [Venstar API Documentation](https://developer.venstar.com/restcalls.html).) Specifically, the T3700 Residential Voyager model with the ACC-VWF1 wi-fi module are used during development.

## Requirements

The following are required:

- Griddy service
- Venstar thermostat with wi-fi module and local API
- linux-based application host (e.g., Raspberry Pi running Raspbian OS)

The application host should have network access to the Venstar device.

## Installation

### Thermostat

Install and configure the Venstar thermostat according to the manufacturer's specifications and your HVAC equipment needs. This is outside the scope of this document; however, the main points are:

1. wiring the thermostat to the furnace control board
2. enabling wi-fi access on the thermostat (not the Skyport cloud service)
3. joining the thermostat to the local network 

### Application

On the application host device, clone the thermostat monitor application from the repository:

```sh
$ git clone https://github.com/hashbanged/thermostat.git
```

Change to the project directory and run the installer with root access:

```sh
$ cd thermostat
$ sudo ./installer.sh
```

The installer will create an application directory in `/opt/thermostat_manager/` and a systemd entry as `/etc/systemd/system/thermostat.service`.

Edit the configuration file, referring to your thermostat IP address and Griddy account to supply connection parameters:

*/opt/thermostat_manager/.env.local*
```sh
THERMOSTAT_ADDRESS=
GRIDDY_METER_ID=
GRIDDY_MEMBER_ID=
GRIDDY_SETTLEMENT_POINT=
```

Enable the systemd service to run the thermostat monitor at startup:

```sh
$ sudo systemctl enable thermostat
```

Issue the start and status commands to run and verify the service:

```sh
$ sudo systemctl start thermostat
$ systemctl status thermostat
```



#### Uninstalling

Remove the application and systemd service by running the installer with the `-u` flag:

```sh
$ sudo ./installer.sh -u
```

---

## Development / testing
*Reference: http://doc.pytest.org/en/latest/*

This is a work in progress and aims toward building a development environment in an easily-reproducible way.

### Pytest installation

Install and verify the Pytest version:

```sh
$ pip3 install -U pytest
$ pytest --version
```

### Setting up the environment

Install `venv`:

```sh
$ sudo apt install python3.7-venv
$ python3 -m venv /path/to/project
```

Create a `setup.py` file in the project root:

```python
from setuptools import setup, find_packages

setup(name="PACKAGENAME", packages=find_packages())
```

Install the project package in editable mode:

```sh
$ pip3 install --editable .
```

### Running tests

Tests are run using Python 3 with:

```sh
$ python3 -m pytest
```
