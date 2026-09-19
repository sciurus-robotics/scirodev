# scirodev

Host-side companion to the PeakHub firmware: **typed API stubs** for the `sciro`
namespace that PeakHub programs import, plus the hub tooling (it depends on
`pybricksdev`, so `scirodev run ble prog.py` works exactly like `pybricksdev`).

```
pip install scirodev                                    # from PyPI
pip install "scirodev @ git+https://github.com/sciurus-robotics/scirodev.git@v0.1.0"
pipx install scirodev                                   # just the CLI, in its own venv
```

Hacking on it (e.g. from the `pybricks-wrap` checkout, where it is a submodule):

```
pip install -e scirodev
```

Then your IDE/type checker knows these, which the upstream `pybricks` stubs don't:

```python
from sciro.parameters import Port          # Port.A .. Port.H (PeakHub has 8 ports)
from sciro.iodevices import PUMPDevice     # generic PUMP device access
from sciro.floorpro import FloorPro        # LP-FloorPro convenience class

fp = FloorPro(Port.G)
cog_dark, cog_bright, brightness, darkness, mask, calibrating = fp.line.read()
```

On the hub these modules are frozen into the PeakHub firmware
(`bricks/peakhub723/modules/sciro` in
[DrTom/pybricks-micropython](https://github.com/DrTom/pybricks-micropython)): `sciro.parameters` and
`sciro.iodevices` re-export the same runtime objects as their `pybricks.*`
counterparts, so `sciro.parameters.Port is pybricks.parameters.Port` — the stubs
only add what the IDE is missing. Keep the two in sync: the stub files here mirror
the frozen modules there.

Protocol reference for the PUMP device API: `PUMP-Protocol.md` in the
`pybricks-wrap` repository.

## Releasing

Bump `version` in `pyproject.toml`, commit, tag `vX.Y.Z` and push the tag. The
GitHub workflow builds, type-checks and publishes to PyPI via Trusted Publishing
(configured on pypi.org: owner `sciurus-robotics`, repo `scirodev`, workflow
`publish.yml`, environment `pypi`).
