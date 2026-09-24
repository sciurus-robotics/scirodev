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
from typing import TYPE_CHECKING

from pybricks.parameters import _PybricksEnum

if TYPE_CHECKING:
    from pybricks.parameters import Port as _Port

    class Port(_Port):
        """Port on the PeakHub. Eight LPF2/PUP ports, A .. H.

        For the type checker this is a subclass of ``pybricks.parameters.Port``
        (on the hub it is the same object), so a ``sciro`` port is accepted
        wherever the upstream stubs expect a ``pybricks.parameters.Port``
        (``Motor``, ``DriveBase``, ...). A .. F are inherited; G and H are
        the two extra PeakHub ports.
        """

        G: Port
        H: Port

else:
    # At runtime the upstream Port is a real Enum, which cannot be subclassed
    # once it has members; tooling that imports the stubs (docs, tests) gets
    # an equivalent enum with all eight ports instead.
    class Port(_PybricksEnum):
        """Port on the PeakHub. Eight LPF2/PUP ports, A .. H."""

        A = ord("A")
        B = ord("B")
        C = ord("C")
        D = ord("D")
        E = ord("E")
        F = ord("F")
        G = ord("G")
        H = ord("H")


class ExtPort:
    """Extension port of a PUMP device (1-based, as in its stream table)."""

    EXT1: int = 1
    EXT2: int = 2
    EXT3: int = 3
    EXT4: int = 4
    EXT5: int = 5
    EXT6: int = 6
