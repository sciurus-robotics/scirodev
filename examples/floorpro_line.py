"""Minimal PeakHub program using the sciro API. Run: scirodev run ble examples/floorpro_line.py"""

from pybricks.tools import wait

from sciro.pump import FloorPro
from sciro.parameters import Port

fp = FloorPro(Port.A)
print("FloorPro", fp.serial, "streams:", len(fp.streams()))

while True:
    cog_dark, cog_bright, brightness, darkness, mask, calibrating = fp.line.read()
    print(cog_dark, brightness)
    wait(100)
