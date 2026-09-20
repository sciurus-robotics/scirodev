"""sciro.floorpro -- deprecated alias of :mod:`sciro.pump` (where the FloorPro
class lives now). Kept so older programs keep type-checking.
"""

from .pump import (  # noqa: F401  (re-exports)
    IMU as IMU,
    ColorSensor as ColorSensor,
    FloorPro as FloorPro,
    IRCalib as IRCalib,
    IRRaw as IRRaw,
    Line as Line,
    Pixels as Pixels,
)
