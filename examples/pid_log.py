"""Experimental sciro.robotics / sciro.tools: log a PID run and publish it as CSV.

Run: scirodev run ble pid_log.py -> writes pid_log.csv next to this script.
The loop below only simulates a first-order plant; on a robot, feed the real
error (setpoint - measurement) and, if you have it, the measured derivative.
"""

from pybricks.tools import wait

from sciro.robotics import PIDController
from sciro.tools import RingBuffer

pid = PIDController(kp=2.0, ki=0.5, kd=0.1, integral_limit=50, output_limit=100, name="demo")
log: RingBuffer = pid.make_log(seconds=2, rate=100)

setpoint = 100.0
value = 0.0
for _ in range(150):
    out = pid.update(setpoint - value)
    value += 0.05 * out  # plant: value follows the output
    wait(10)

print("rows:", len(log), "last:", log[-1])
log.publish("pid_log.csv")
