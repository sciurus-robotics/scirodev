"""sciro.hubs -- the PeakHub.

On the hub this module re-exports ``pybricks.hubs`` unchanged; the stub adds what
the upstream stubs lack: the ``PeakHub`` class, its ``display.device()``, and the
``ThisHub`` alias.
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


class UsbPd:
    """**Experimental.** The hub's USB-PD input.

    Reached as :attr:`PeakHub.usb_pd`. Lets a program read the measured input
    voltage and ask the USB-PD sink to renegotiate to a different one.
    """

    def voltage(self, volts: Optional[int] = None) -> Optional[int]:
        """voltage(volts=None) -> int

        Without an argument, returns the **measured** USB-PD input voltage in
        millivolts. The sense sits before the ideal diode, so it reads the
        supply itself and is not masked by a connected battery. Returns 0 if
        the ADC has not sampled yet (only in the first few ms after boot).

        With an argument, asks the sink to renegotiate to that voltage.

        Arguments:
            volts (int): 5, 9, 12 or 15. Any other value raises ``ValueError``.

        Returns:
            The measured voltage in mV when called with no argument,
            otherwise ``None``.

        .. warning::

            **Experimental, and it is a request rather than a command.**

            A supply that does not offer the requested voltage simply refuses.
            Nothing is raised in that case and the hub stays where it was, so
            **read the voltage back** to see what actually happened rather than
            assuming the call took effect.

            Higher PD gears (20 V, 28 V) are deliberately unreachable: the
            hub's voltage sense saturates at 18.81 V, so the firmware could not
            even measure what it had asked for.

        Renegotiating itself is well behaved in practice: measured working even
        while driving motors on a small (2x18650-class) power bank, and on a
        bench supply switching 9 V to 12 V and back with the hub up throughout.
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
    usb_pd = UsbPd()

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


#: The hub this program is running on.
#:
#: Every Pybricks firmware compiles in exactly one hub class and exports it
#: under several names: the generic ``ThisHub``, the hub's own name, and any
#: aliases. On PeakHub firmware ``ThisHub``, :class:`PeakHub`, ``PrimeHub`` and
#: ``InventorHub`` are therefore all the *same* class object -- this is resolved
#: when the firmware is built, not by detecting anything at run time.
#:
#: Use it for code that should run unchanged on whichever hub is in front of
#: you, which is mostly bench and test scripts::
#:
#:     from sciro.hubs import ThisHub
#:
#:     hub = ThisHub()
#:     print(hub.imu.heading(), hub.imu.tilt())
#:
#: Prefer :class:`PeakHub` when a program is specific to this hub anyway: it
#: says so, and it reads better than a generic name.
#:
#: Note the difference between the REPL and a downloaded program. The REPL is
#: started with everything auto-imported and with a ready-made ``hub`` instance
#: already created, so there ``hub.imu.heading()`` just works. A downloaded
#: program gets neither: it must import what it uses and construct the hub, as
#: above, and ``print(hub)`` there raises ``NameError``. (In the firmware this
#: is ``pb_package_pybricks_init(true)`` for the REPL versus ``false`` for
#: everything else.)
ThisHub = PeakHub
