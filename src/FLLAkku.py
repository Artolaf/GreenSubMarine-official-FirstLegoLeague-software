# LEGO type:standard slot:1 autostart

from spike import PrimeHub
from hub import battery

Karsten = PrimeHub()

power = battery.voltage()
Karsten.light_matrix.write(power)
print(power)

raise RuntimeError('intentional abort: end of programm')