"""sciro.parameters -- the Pybricks parameter types, with the PeakHub port set.

On the hub this module re-exports ``pybricks.parameters`` unchanged (the firmware
has always had ``Port.G`` and ``Port.H``); this stub exists because the upstream
stubs declare ``Port.A`` .. ``Port.F`` only.
"""

from pybricks.parameters import (  # noqa: F401  (re-exports)
    Axis as Axis,
    Button as Button,
    Color as Color,
    Direction as Direction,
    Icon as Icon,
    Side as Side,
    Stop as Stop,
)
from pybricks.parameters import Port as _Port


class Port(_Port):
    """Port on the PeakHub. Eight LPF2/PUP ports, A .. H.

    A subclass of ``pybricks.parameters.Port`` in the stub only (the same
    object on the hub), so a ``sciro`` port is accepted wherever the upstream
    stubs expect a ``pybricks.parameters.Port`` (``Motor``, ``DriveBase``, ...).
    """

    # A .. F are inherited; the two extra PeakHub ports (stub declarations,
    # the firmware provides the values).
    G: Port
    H: Port


class ExtPort:
    """Extension port of a PUMP device (1-based, as in its stream table)."""

    EXT1: int = 1
    EXT2: int = 2
    EXT3: int = 3
    EXT4: int = 4
    EXT5: int = 5
    EXT6: int = 6
