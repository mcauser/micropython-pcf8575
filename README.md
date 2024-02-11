# MicroPython PCF8575

A MicroPython library for PCF8575 16-Bit I2C I/O Expander with Interrupt.

![demo](docs/demo.jpg)

The PCF8575 consists of a 16-bit quasi-bidirectional port and an I2C-bus interface.

The device includes latched outputs with high current drive capability for directly driving LEDs.

The interrupt has an open-drain output, which means you need a pull-up on your microcontroller
to detect when the PCF8575 drives it LOW.

When setting a pin HIGH, it acts as both output AND input. The pin internally uses a weak
current-source pull-up to latch output HIGH.
When driven LOW, for example, with a push button, the pin will read as LOW.

An interrupt fires on any rising or falling edge of the pins in input mode (HIGH).
Interrupt is cleared when the pins are changed or the port is read.

The pins are labelled P00-P07 for port A and P10-P17 for port B.
When using the pin() method, there is no pins 8-9.
Port B's numbering scheme starts at 10 so the right-most digit for both ports is 0-7.

When accessing the 16-bit port directly, there is no gaps. bit0 is P00 and bit8 is P10.

At power on, all pins are driven HIGH and can be immediately used as inputs.

Operating voltage: 2.5V - 5.5V


## Installation

Using mip via mpremote:

```bash
$ mpremote mip install github:mcauser/micropython-pcf8575
$ mpremote mip install github:mcauser/micropython-pcf8575/examples
```

Using mip directly on a WiFi capable board:

```python
>>> import mip
>>> mip.install("github:mcauser/micropython-pcf8575")
>>> mip.install("github:mcauser/micropython-pcf8575/examples")
```

Manual installation:

Copy `src/pcf8575.py` to the root directory of your device.


## Examples

**Basic Usage**

```python
import pcf8575
from machine import I2C, Pin

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
pcf.port
# returns 65280 (0xFF00)
```

For more detailed examples, see [examples](/examples).

If you mip installed them above, you can run them like so:

```python
import pcf8575.examples.basic
```

## Methods

Construct with a reference to I2C and set the device address.
Valid address range 0x20-0x27.
If are you not sure what it is, run an `i2c.scan()`.
See below for address selection.
```python
__init__(i2c, address=0x20)
```

Scans the I2C bus for the provided address and returns True if a device is present
otherwise raises an OSError.
```python
check()
```

Method for getting or setting a single pin.
If no value is provided, the port will be read and value of specified pin returned.
If a value is provided, the port will be updated and device written to.
The port is written to after each call. If you intend to toggle many pins at once, use the
port property instead. See below.
Valid pin range 0-7 and 10-17.
```python
pin(pin, value=None)
```

Method for flipping the value of a single pin.
Valid pin range 0-7 and 10-17.
```python
toggle(pin)
```

Private method for checking the supplied pin number is within valid ranges.
```python
_validate_pin()
```

Private method for loading _port from the device.
```python
_read()
```

Private method for sending _port to the device.
```python
_write()
```


## Properties

Getter reads the port from the device and returns a 16 bit integer.
```python
port
```

Setter writes a 16-bit integer representing the port to the device.
If you are setting multiple pins at once, use this instead of the pin() method as
this writes the entire 16-bit port to the device once, rather than 16 separate writes.
```python
port = 0xFFFF
```


## Ports

* P00-P07 - Port A
* P10-P17 - Port B

Why is there no P08 and P09? Because they skipped them when naming the pins,
so that the lest significant digit is 0-7 for both ports. There's still only 16 bits.
Port B pins are just labelled +2.

This chip only has two ports (16 pins). If you only need 8 pins, the
[PCF8574](https://github.com/mcauser/micropython-pcf8574) has a single port (8 pins).


## Interrupts

* INT - Active LOW

Shared by both ports A and B. Triggered by either.


## I2C Interface

If you are using a module, most contain 10k pull-ups on the SCL and SDA lines.

If you are using the PCF8575 chip directly, you'll need to add your own.


### I2C Address

The chip supports I2C addresses 0x20-0x27 and is customisable using address pins A0, A1, A2

A0  | A1  | A2  | I2C Address
----|-----|-----|------------
GND | GND | GND | 0x20 (default)
3V3 | GND | GND | 0x21
GND | 3V3 | GND | 0x22
3V3 | 3V3 | GND | 0x23
GND | GND | 3V3 | 0x24
3V3 | GND | 3V3 | 0x25
GND | 3V3 | 3V3 | 0x26
3V3 | 3V3 | 3V3 | 0x27


## Parts

* [PCF8575 blue module](https://s.click.aliexpress.com/e/_DdXNOaN)
* [PCF8575 blue module](https://s.click.aliexpress.com/e/_DFBcPc5)
* [PCF8575 blue module](https://s.click.aliexpress.com/e/_DDFiuqV)
* [PCF8575 red module](https://s.click.aliexpress.com/e/_DmRWVFx)
* [PCF8575 10x SSOP-24](https://s.click.aliexpress.com/e/_DDBKEJP)
* [TinyPICO](https://www.tinypico.com/)


## Connections

### TinyPICO ESP32

```python
from machine import SoftI2C, Pin
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

from machine import I2C, Pin
i2c = I2C(0)
```

PCF8575 Module | TinyPICO (ESP32)
-------------- | ----------------
SDA            | 21 (SDA)
SCL            | 22 (SCL)
VCC            | 3V3
GND            | GND
INT (optional) | 4


## Links

* [micropython.org](http://micropython.org)
* [PCF8575 datasheet](docs/pcf8575.pdf)
* [TinyPICO Getting Started](https://www.tinypico.com/gettingstarted)


## License

Licensed under the [MIT License](http://opensource.org/licenses/MIT).

Copyright (c) 2019 Mike Causer
