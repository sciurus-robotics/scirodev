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
from pybricks.parameters import _PybricksEnum


class Port(_PybricksEnum):
    """Port on the PeakHub. Eight LPF2/PUP ports, A .. H."""

    A: Port = ord("A")
    B: Port = ord("B")
    C: Port = ord("C")
    D: Port = ord("D")
    E: Port = ord("E")
    F: Port = ord("F")
    G: Port = ord("G")
    H: Port = ord("H")


class ExtPort:
    """Extension port of a PUMP device (1-based, as in its stream table)."""

    EXT1: int = 1
    EXT2: int = 2
    EXT3: int = 3
    EXT4: int = 4
    EXT5: int = 5
    EXT6: int = 6
