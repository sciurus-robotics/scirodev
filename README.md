# scirodev

Host-side companion to Sciurus Robotics hubs (PeakHub so far): **typed API
stubs** for the `sciro` namespace that PeakHub programs import, plus the
`scirodev` command line tool.

The tool is built on `pybricksdev`. It offers pybricksdev's own tools
unchanged (`scirodev run ble prog.py` works exactly like `pybricksdev run`),
and adds tools that only exist for sciro hubs, such as `scirodev rename`.
`scirodev -h` lists both and marks which is which.

```
pip install scirodev                                    # from PyPI
pip install "scirodev @ git+https://github.com/sciurus-robotics/scirodev.git@v0.1.0"
pipx install scirodev                                   # just the CLI, in its own venv
```

Hacking on it:

```
pip install -e .
```

Then your IDE/type checker knows these, which the upstream `pybricks` stubs don't:

```python
from sciro.parameters import Port          # Port.A .. Port.H (PeakHub has 8 ports)
from sciro.iodevices import PUMPDevice     # generic PUMP device access
from sciro.pump import FloorPro        # PUMP devices (LP-FloorPro, ...)
from sciro.hubs import PeakHub             # hub class incl. display.device()
from sciro.canbus import CAN               # beta: raw classic-CAN frames on connector 1/2
from sciro.tools import RingBuffer         # experimental: RAM recorder -> CSV file via the console
from sciro.robotics import PIDController   # experimental: PID with optional logging

hub = PeakHub()
fp = FloorPro(Port.G)
cog_dark, cog_bright, brightness, darkness, mask, calibrating = fp.line.read()
hub.display.device(fp, brightness=50)      # mirror the sensor's LED strip on the 5x5
```

Experimental (API may change): a RAM recorder that publishes CSV through the
console, and a PID controller that can log into it:

```python
from sciro.robotics import PIDController
from sciro.tools import RingBuffer

pid = PIDController(kp=15, kd=0.2, output_limit=300)
log = pid.make_log(seconds=10, rate=100)     # RingBuffer of pid.LOG_FIELDS
turn_rate = pid.update(error, derivative=-hub.imu.angular_velocity(Axis.Z))
log.publish("doc/pid_run.csv")               # scirodev run writes the file next to the script
```

The drivebase's own controllers log too (built into Pybricks, undocumented
upstream): `db.heading_control.log.start(5000, down_sample=2)` records the
reference trajectory, the estimated state and the P/I/D terms at 100 Hz from the
firmware's control loop; `db.heading_control.log.publish("heading.csv")` writes
it with a header line. `sciro.robotics.DriveBase` is the Pybricks class with
these attributes typed. `log.record(db.state)` is the coroutine form for
anything else.

`publish(path)` wraps the CSV in pybricksdev's `_file_begin_ <path>` /
`_file_end_` lines; `scirodev run` (and `pybricksdev run`) then write the block
to that file, relative to the script's folder, instead of echoing it. Without a
path the CSV goes to the terminal.

Full demo programs for the LP FloorPro (both for LEGO hubs and the PeakHub) live in
[sciurus-robotics/FloorPro-CodeDemos](https://github.com/sciurus-robotics/FloorPro-CodeDemos);
`examples/` here stays minimal.

On the hub these modules are frozen into the PeakHub firmware:
`sciro.parameters` and `sciro.iodevices` re-export the same runtime objects as
their `pybricks.*` counterparts, so `sciro.parameters.Port is
pybricks.parameters.Port` — the stubs only add what the IDE is missing. The
stub files here mirror the frozen modules; a release of this package matches
the PeakHub firmware of the same date.

## Hub names

Every PeakHub advertises under its own name, `Peak-XXXX` out of the box (the
first four characters of its board ID), so several hubs on one table can be
told apart:

```
scirodev run ble --name Peak-BYN9 prog.py
```

Give a hub a name of your choice (1 to 16 printable ASCII characters); it is
stored on the hub and survives power cycles and firmware updates:

```
scirodev rename usb MyRobot               # over USB: applied at once
scirodev rename ble MyRobot -n Peak-BYN9  # over Bluetooth: confirm on the hub
scirodev rename usb --default             # back to Peak-XXXX
```

Over Bluetooth the hub spells the new name on its display, then shows `?`.
Press the center button to accept; any other button, or 10 seconds without
one, rejects. This keeps somebody else in radio range from renaming your hub.
`hub.system.name()` returns the name.

## API reference (HTML)

The stubs double as the source of the API reference, built with Sphinx the way
docs.pybricks.com is (cross-links into it for the upstream types):

```
pip install -e ".[docs]"
scripts/build-docs            # -> docs/_build/html/index.html
```

The build output is static HTML; a website can copy that folder as is.

## Releasing

Bump `version` in `pyproject.toml`, commit, tag `vX.Y.Z` and push the tag. The
GitHub workflow builds, type-checks and publishes to PyPI via Trusted Publishing
(configured on pypi.org: owner `sciurus-robotics`, repo `scirodev`, workflow
`publish.yml`, environment `pypi`).
