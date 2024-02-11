# SPDX-FileCopyrightText: 2019 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython PCF8575 LEDs sourcing current example

Connect a LED between P00 and GND.
* LED positive anode (long leg) connected to P00.
* LED negative cathode (short leg) connected to GND.

Driving a pin HIGH will illuminate the LED.

The device has latched outputs with high current drive capability
for directly driving LEDs.
"""

import pcf8575
from machine import I2C

# TinyPICO (ESP32)
i2c = I2C(0)

pcf = pcf8575.PCF8575(i2c, 0x20)

# set P00 HIGH and all other pins LOW
# turn LED on
pcf.port = 0x0001

# turn LED off
pcf.port = 0x0000
