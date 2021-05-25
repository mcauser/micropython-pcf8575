"""
MicroPython PCF8575 16-Bit I2C I/O Expander with Interrupt
https://github.com/mcauser/micropython-pcf8575

MIT License
Copyright (c) 2019 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class PCF8575:
    def __init__(self, i2c, address=0x20):
        self._i2c = i2c
        self._address = address
        self._port = bytearray(2)
        if i2c.scan().count(address) == 0:
            raise OSError('PCF8575 not found at I2C address {:#x}'.format(address))

    @property
    def port(self):
        self._read()
        return self._port[0] | (self._port[1] << 8)

    @port.setter
    def port(self, value):
        self._port[0] = value & 0xff
        self._port[1] = (value >> 8) & 0xff
        self._write()

    def pin(self, pin, value=None):
        pin = self.validate_pin(pin)
        if value is None:
            self._read()
            return (self._port[pin // 8] >> (pin % 8)) & 1
        else:
            if value:
                self._port[pin // 8] |= (1 << (pin % 8))
            else:
                self._port[pin // 8] &= ~(1 << (pin % 8))
            self._write()

    def toggle(self, pin):
        # pin valid range 0..7 and 10-17 (shifted to 8-15)
        pin = self.validate_pin(pin)
        self._port[pin // 8] ^= (1 << (pin % 8))
        self._write()

    def validate_pin(self, pin):
        if not 0 <= pin <= 7 and not 10 <= pin <= 17:
            raise ValueError('Invalid pin {}. Use 0-7 or 10-17.'.format(pin))
        if pin >= 10:
            pin -= 2
        return pin

    def _read(self):
        self._i2c.readfrom_into(self._address, self._port)

    def _write(self):
        self._i2c.writeto(self._address, self._port)