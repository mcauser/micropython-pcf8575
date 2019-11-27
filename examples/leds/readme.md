# LEDs

## Sourcing current

Connect a LED between P00 and GND.

LED positive anode (long leg) connected to P00.

LED negative cathode (short leg) connected to GND.

Driving a pin HIGH will illuminate the LED.

The device has latched outputs with high current drive capability
for directly driving LEDs.

Can sink 25mA.

```python
import pcf8575
from machine import Pin, I2C

# TinyPICO
i2c = I2C(scl=Pin(22), sda=Pin(21))

pcf = pcf8575.PCF8575(i2c, 0x20)

# set P00 HIGH and all other pins LOW
# turn LED on
pcf.port = 0x0001

# turn LED off
pcf.port = 0x0000
```

## Sinking current

Connect a LED between P01 and 3V3, via a resistor.

LED positive anode (long leg) connected to 3V3.

LED negative cathode (short leg) connected to P01.

Driving a pin LOW will illuminate the LED.

For a red or blue LED, use a 330K and green LED 220K current limiting resistor.

Can source 100mA.

```python
import pcf8575
from machine import Pin, I2C

# TinyPICO
i2c = I2C(scl=Pin(22), sda=Pin(21))

pcf = pcf8575.PCF8575(i2c, 0x20)

# set P01 LOW and all other pins HIGH
# turn LED on
pcf.port = 0xfffd

# turn LED off
pcf.port = 0xffff
```
