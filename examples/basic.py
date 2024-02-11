# SPDX-FileCopyrightText: 2019 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython PCF8575 Basic example

Toggles pins individually, then all in a single call
"""

import pcf8575
from machine import I2C

# TinyPICO (ESP32)
i2c = I2C(0)

pcf = pcf8575.PCF8575(i2c, 0x20)

# read pin 2
pcf.pin(2)

# set pin 3 HIGH
pcf.pin(3, 1)

# set pin 4 LOW
pcf.pin(4, 0)

# toggle pin 5
pcf.toggle(5)

# set all pins at once with 16-bit int
pcf.port = 0xFF00

# read all pins at once as 16-bit int
print(pcf.port)
# returns 65280 (0xFF00)
