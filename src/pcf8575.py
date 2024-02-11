# SPDX-FileCopyrightText: 2019 Mike Causer <https://github.com/mcauser>
# SPDX-License-Identifier: MIT

"""
MicroPython PCF8575 16-Bit I2C I/O Expander with Interrupt
https://github.com/mcauser/micropython-pcf8575
"""

__version__ = "1.1.0"


class PCF8575:
    def __init__(self, i2c, address=0x20):
        self._i2c = i2c
        self._address = address
        self._port = bytearray(2)

    def check(self):
        if self._i2c.scan().count(self._address) == 0:
            raise OSError(f"PCF8575 not found at I2C address {self._address:#x}")
        return True

    @property
    def port(self):
        self._read()
        return self._port[0] | (self._port[1] << 8)

    @port.setter
    def port(self, value):
        self._port[0] = value & 0xFF
        self._port[1] = (value >> 8) & 0xFF
        self._write()

    def pin(self, pin, value=None):
        pin = self._validate_pin(pin)
        if value is None:
            self._read()
            return (self._port[pin // 8] >> (pin % 8)) & 1
        if value:
            self._port[pin // 8] |= 1 << (pin % 8)
        else:
            self._port[pin // 8] &= ~(1 << (pin % 8))
        self._write()

    def toggle(self, pin):
        pin = self._validate_pin(pin)
        self._port[pin // 8] ^= 1 << (pin % 8)
        self._write()

    def _validate_pin(self, pin):
        # pin valid range 0..7 and 10-17 (shifted to 8-15)
        # first digit: port (0-1)
        # second digit: io (0-7)
        if not 0 <= pin <= 7 and not 10 <= pin <= 17:
            raise ValueError(f"Invalid pin {pin}. Use 0-7 or 10-17.")
        if pin >= 10:
            pin -= 2
        return pin

    def _read(self):
        self._i2c.readfrom_into(self._address, self._port)

    def _write(self):
        self._i2c.writeto(self._address, self._port)
