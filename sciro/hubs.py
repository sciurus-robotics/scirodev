"""sciro.hubs -- the PeakHub.

On the hub this module re-exports ``pybricks.hubs`` unchanged; the stub adds what
the upstream stubs lack: the ``PeakHub`` class and its ``display.device()``.
"""

from __future__ import annotations

from typing import Any, Optional, Protocol, Tuple

from pybricks import _common
from pybricks.hubs import PrimeHub as PrimeHub  # noqa: F401  (re-export)
from pybricks.parameters import Axis as _Axis
from pybricks.parameters import Button as _Button

from .iodevices import PUMPDevice


class DisplaySource(Protocol):
    """Anything :meth:`LightMatrix.device` can show: an object whose
    ``_display_source()`` returns ``(PUMPDevice, stream id, map)``.
    """

    def _display_source(self) -> Tuple[PUMPDevice, int, Tuple[Optional[int], ...]]: ...


class LightMatrix(_common.LightMatrix):
    """The PeakHub's 5x5 RGB matrix: everything ``pybricks`` offers, plus a
    background mirror of a PUMP device's display stream.
    """

    def device(self, device: DisplaySource, brightness: int = 100) -> None:
        """device(device, brightness=100)

        Shows the device's own display (e.g. the LP-FloorPro's LED strip) on
        the matrix, updated in the background at the device's rate until
        :meth:`off` or any other drawing call. The device stops streaming when
        the program ends.

        Arguments:
            device (FloorPro): The device to mirror (any ``sciro.pump`` device with a display stream).
            brightness (Number, %): Brightness of the mirrored pixels, 0 .. 1000.
                Above 100 the picture is amplified (clipping at full), since
                the matrix is far dimmer than a sensor's own LED strip.
        """


class PeakHub:
    """LEGO-compatible hub by Sciurus Robotics: 8 ports, 5x5 RGB matrix, IMU."""

    # Class attributes for documentation/typing only; the firmware creates
    # them as instance attributes in __init__.
    battery = _common.Battery()
    buttons = _common.Keypad([_Button.LEFT, _Button.RIGHT, _Button.CENTER, _Button.BLUETOOTH])
    charger = _common.Charger()
    display = LightMatrix(5, 5)
    imu = _common.IMU()
    speaker = _common.Speaker()
    system = _common.System()
    ble = _common.BLE()

    def __init__(
        self,
        top_side: Any = _Axis.Z,
        front_side: Any = _Axis.X,
        broadcast_channel: int = 0,
        observe_channels: Any = (),
    ):
        """PeakHub(top_side=Axis.Z, front_side=Axis.X, broadcast_channel=0, observe_channels=[])

        Arguments:
            top_side (Axis): The axis that passes through the *top side* of the hub.
            front_side (Axis): The axis that passes through the *front side* of the hub.
            broadcast_channel: Channel for broadcasting data (0 .. 255).
            observe_channels: Channels to observe.
        """
