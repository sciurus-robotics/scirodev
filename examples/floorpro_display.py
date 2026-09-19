"""Mirror the LP-FloorPro's LED strip on the PeakHub's 5x5 matrix.
Run: scirodev run ble examples/floorpro_display.py"""

from pybricks.tools import wait

from sciro.floorpro import FloorPro
from sciro.hubs import PeakHub
from sciro.parameters import Port

hub = PeakHub()
fp = FloorPro(Port.A)

# Rows 0-2: the 15 IR channels; bottom corners: EXT1 / EXT2; bottom centre: battery.
hub.display.device(fp, brightness=50)

while True:
    cog_dark, cog_bright, brightness, darkness, mask, calibrating = fp.line.read()
    print(cog_dark, cog_bright)
    wait(200)
