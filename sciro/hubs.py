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


    def on(self, brightness: int = 100) -> None:
        """on(brightness=100)

        Turns all pixels on at ``brightness`` percent (0 .. 100), stopping a
        running :meth:`device` mirror or animation. Declared here because the
        firmware has it while the published ``pybricks`` stubs do not.
        """


class System(_common.System):
    """The PeakHub's system object: everything ``pybricks`` offers, plus the
    board identity.
    """

    def device_id(self) -> str:
        """device_id() -> str

        The full factory unique ID of the hub's MCU as a 24-character uppercase
        hex string. Stable per physical hub.
        """

    def short_id(self) -> str:
        """short_id() -> str

        The hub's 8-character short ID (Crockford base32, derived from the
        device ID): the same value the boot console prints and the device
        inventory uses.
        """

    def info(self) -> dict:
        """info() -> dict

        ``{"name", "device_id", "short_id", "reset_reason", "program_id",
        "program_start_type"}`` in one call.
        """

    def name(self) -> str:
        """name() -> str

        The hub name, as advertised over Bluetooth.
        """

    def reset_reason(self) -> int:
        """reset_reason() -> int

        Why the hub last reset: ``0`` power-on or unknown, ``1`` software
        reset, ``2`` watchdog.
        """

    def low_power(self) -> None:
        """low_power()

        Ends the program and drops the hub into its wakeable low-power mode
        (device supply off, motors coasting, panel dimmed) instead of powering
        off; a short button press wakes it back to the idle menu. PeakHub only.
        """


class Battery(_common.Battery):
    """The PeakHub's battery, with the two readings the published ``pybricks``
    stubs lack."""

    def type(self) -> str:
        """type() -> str

        The battery chemistry the hub was built for: ``"Li-ion"``,
        ``"Alkaline"`` or ``"Unknown"``.
        """

    def temperature(self) -> int:
        """temperature() -> int

        The battery pack temperature, in milli-degrees Celsius.
        """


class PeakHub:
    """LEGO-compatible hub by Sciurus Robotics: 8 ports, 5x5 RGB matrix, IMU."""

    # Class attributes for documentation/typing only; the firmware creates
    # them as instance attributes in __init__.
    # No charger and no ble: the firmware's hub type exposes neither (the
    # PeakHub's Bluetooth is a console/protocol transport, not a user API).
    battery = Battery()
    buttons = _common.Keypad([_Button.LEFT, _Button.RIGHT, _Button.CENTER, _Button.BLUETOOTH])
    display = LightMatrix(5, 5)
    imu = _common.IMU()
    speaker = _common.Speaker()
    system = System()

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
