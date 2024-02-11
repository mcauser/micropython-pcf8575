# SPDX-FileCopyrightText: 2019 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython PCF8575 LEDs sinking current example

Connect a LED between P01 and 3V3, via a current limiting resistor.
* LED positive anode (long leg) connected to 3V3.
* LED negative cathode (short leg) connected to P01.

Driving a pin LOW will illuminate the LED.

eg. for a red or blue LED, use a 330K and green LED 220K current limiting resistor.
"""

import pcf8575
from machine import I2C

# TinyPICO (ESP32)
i2c = I2C(0)

pcf = pcf8575.PCF8575(i2c, 0x20)

# set P01 LOW and all other pins HIGH
# turn LED on
pcf.port = 0xFFFE

# turn LED off
pcf.port = 0xFFFF
