# scirodev

Host-side companion to the PeakHub firmware: **typed API stubs** for the `sciro`
namespace that PeakHub programs import, plus the hub tooling (it depends on
`pybricksdev`, so `scirodev run ble prog.py` works exactly like `pybricksdev`).

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

## Releasing

Bump `version` in `pyproject.toml`, commit, tag `vX.Y.Z` and push the tag. The
GitHub workflow builds, type-checks and publishes to PyPI via Trusted Publishing
(configured on pypi.org: owner `sciurus-robotics`, repo `scirodev`, workflow
`publish.yml`, environment `pypi`).
