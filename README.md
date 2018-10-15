# PomoLux
### Pomodoro timer with batteries.
> It randomly picks and runs a playlist along with the timer; the dafault music source comes from `musicforprogramming.net`. When present a Luxafor Flag is ran according to the user's busy state.

> All the modules can also be ran standalone.

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
