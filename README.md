# PomoLux
> Pomodoro timer with batteries. It randomly picks and runs along the timer a playlist from `musicforprogramming.net`; and when present it sets a Luxafor Flag according to the user's busy state.

All the present modules can be ran standalone as well as along the `pomodoro timer`.

## Pomodoro timer

* Clone this repo.
* Run `./pomodoro --help` for a quick list of options.
* Follow the instructions displayed to modify times and cycles to your liking.

## Python API for the Luxafor Flag

* Run `./python_luxafor.py --help` for a quick list of options.
* Alternatively instantiate the LuxaforDev class and send the bytes list of your choice to the device:
``` Python
from  python_luxafor import LuxaforDev
lux = LuxaforDev()
lux.work()
lux.off()
lux.write([6, 5, 1, 0, 0, 0, 0])
```
