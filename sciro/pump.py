"""sciro.pump -- PUMP devices on the PeakHub, the PUMP counterpart of
``pybricks.pupdevices``: the generic :class:`PUMPDevice` plus one class per
device (currently the LP-FloorPro line sensor).

Stub for the frozen module of the same name. Every reading method returns the
value directly, or an awaitable under multitasking.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional, Tuple, Union

if TYPE_CHECKING:
    from pybricks._common import MaybeAwaitable, MaybeAwaitableColor, MaybeAwaitableFloat

    from ._common import (
        MaybeAwaitableEuler,
        MaybeAwaitableInts,
        MaybeAwaitableIRCalib,
        MaybeAwaitableLine,
        MaybeAwaitablePixels,
        MaybeAwaitableRGB8,
        MaybeAwaitableCalibration,
        MaybeAwaitableStr,
        MaybeAwaitableRGBC,
    )

from .iodevices import PUMPDevice as PUMPDevice  # noqa: F401  (re-export)
from .iodevices import StreamInfo
from pybricks.parameters import Color

from .parameters import Port as _Port


class _Stream:
    dev: PUMPDevice
    id: int

    def subscribe(self, mode: int, rate: int = 0) -> MaybeAwaitable:
        """subscribe(mode, rate=0)  -- rate in Hz, 0 = every sample; see :meth:`PUMPDevice.subscribe`."""

    def state(self) -> Optional[bytes]:
        """state() -> bytes | None  -- the stream's current state prefix."""


class Line(_Stream):
    """IR array derived data (default: every sample, 400 Hz)."""

    def read(self) -> MaybeAwaitableLine:
        """read() -> Tuple

        Returns ``(cog_dark, cog_bright, brightness, darkness, mask, calibrating)``:
        centre of gravity of the dark / bright pixels in sensor pitches from the
        middle sensor (-7 .. +7), overall brightness / darkness (0 .. 1), a
        15-bit bright-pixel mask (bit i = sensor i), and whether calibration is
        active.
        """

    def calibrate(self, enable: bool = True) -> MaybeAwaitable:
        """calibrate(enable=True)  -- start/stop min-max calibration of the array."""


class IRRaw(_Stream):
    """15 raw 12-bit ADC readings. Off by default: use :meth:`oneshot` or subscribe."""

    def read(self) -> MaybeAwaitableInts:
        """read() -> Tuple[int, ...]  -- 15 values, 0 .. 4095, sensor 0 first."""

    def oneshot(self) -> MaybeAwaitableInts:
        """oneshot() -> Tuple[int, ...]  -- request one frame and return it."""


class IRCalib(_Stream):
    """Calibration table of the IR array. Off by default."""

    def read(self) -> MaybeAwaitableIRCalib:
        """read() -> Tuple

        Returns ``(min, max, min_visited_mask, max_visited_mask)`` with ``min`` and
        ``max`` tuples of 15 raw counts.
        """

    def oneshot(self) -> MaybeAwaitableIRCalib:
        """oneshot() -> Tuple  -- request the table once and return it."""


class Pixels(_Stream):
    """The sensor's own LED strip picture, rendered on the device at full scale:
    18 ``(r, g, b)`` triplets = IR channels 0..14, EXT1, EXT2, battery. Off by
    default. A PeakHub mirrors it on its 5x5 matrix with
    :meth:`sciro.hubs.LightMatrix.device`.
    """

    def read(self) -> MaybeAwaitablePixels:
        """read() -> Tuple[Tuple[int, int, int], ...]  -- 18 RGB triplets, 0 .. 255."""

    def oneshot(self) -> MaybeAwaitablePixels:
        """oneshot() -> Tuple  -- request one frame and return it."""


class ColorSensor(_Stream):
    """TCS3400 colour sensor on an extension port of a PUMP device.

    ``ColorSensor(port, ext_port)`` opens it directly; :meth:`FloorPro.color_sensor`
    returns the same class. ``hsv()`` and ``color()`` follow
    ``pybricks.pupdevices.ColorSensor``.

    Every sample is tagged with the settings it was measured under, so a read
    after a settings change waits for the first sample taken with the new
    settings.
    """

    ext_port: int

    def __init__(self, port: Union[_Port, PUMPDevice], ext_port: int = 1):
        """ColorSensor(port, ext_port=ExtPort.EXT1)

        Arguments:
            port (Port): Hub port of the PUMP device carrying the sensor (or the
                opened ``PUMPDevice`` itself).
            ext_port (ExtPort): Extension port the sensor is plugged into.
                Raises ``OSError`` if there is no colour sensor there.
        """

    def read(self) -> MaybeAwaitableRGBC:
        """read() -> Tuple[int, int, int, int, int]  -- raw (red, green, blue, clear, status) at device resolution."""

    def calibrated(self) -> MaybeAwaitableRGB8:
        """calibrated() -> Tuple[int, int, int]

        Red, green, blue 0 .. 255 as the device itself shows them: stretched
        over the calibrated range when a valid calibration applies, scaled to
        full scale otherwise.
        """

    def hsv(self) -> MaybeAwaitableColor:
        """hsv() -> Color

        Hue (0 .. 359), saturation (0 .. 100) and value (0 .. 100) of the
        surface, as a ``Color``: standard HSV of the calibrated colour when a
        valid calibration applies, of the raw reading otherwise.
        """

    def calibration_status(self) -> MaybeAwaitableStr:
        """calibration_status() -> str

        ``"none"`` (nothing stored), ``"weak"`` (stored but not applicable:
        incomplete, or LED / gain / integration differ from the calibration
        profile), ``"ok"`` (applied), or ``"calibrating"``.
        """

    def calibrate(self, enable: bool = True) -> MaybeAwaitable:
        """calibrate(enable=True)

        Start or stop the range calibration on the device. While it runs, move
        the sensor over the darkest and brightest surfaces (or elements) it
        will see; stopping stores the table on the sensor, bound to the LED,
        gain and integration time in force. Changing those meanwhile aborts it.
        """

    def clear_calibration(self) -> MaybeAwaitable:
        """clear_calibration()  -- drop the stored calibration (back to full-scale colour)."""

    def calibration(self) -> MaybeAwaitableCalibration:
        """calibration() -> Tuple

        The stored table: ``(min, max, (led, gain, atime), valid, applicable,
        visited_mask)`` with ``min``/``max`` tuples of four counts (red, green,
        blue, clear). Fetched from the device on demand.
        """

    def color(self) -> MaybeAwaitableColor:
        """color() -> Color

        The nearest of the detectable colours (default: red, yellow, green,
        blue, white, none), matched like ``pybricks.pupdevices.ColorSensor``.
        """

    def detectable_colors(self, colors: Optional[Iterable[Color]] = None) -> Optional[Tuple[Color, ...]]:
        """detectable_colors(colors)  -- set the colours color() chooses from; with no argument, get them."""

    def settings(self) -> Tuple[int, int, int]:
        """settings() -> Tuple[int, int, int]  -- (led_percent, gain_x, atime) in effect."""

    def set_light(self, percent: int) -> MaybeAwaitable:
        """set_light(percent)  -- illumination LED duty, 0 .. 100."""

    def set_gain(self, gain_x: int) -> MaybeAwaitable:
        """set_gain(gain_x)  -- analog gain: 1, 4, 16 or 64."""

    def set_integration(self, atime: int) -> MaybeAwaitable:
        """set_integration(atime)  -- TCS3400 ATIME register 0 .. 255: (256 - atime) * 2.78 ms."""


class Gyro(_Stream):
    """Gyro (BNO086) on an extension port of a PUMP device: roll, pitch, yaw in degrees.

    ``Gyro(port, ext_port)`` opens it directly; :meth:`FloorPro.gyro` returns the
    same class (``IMU`` is an alias). The heading offset lives on the hub:
    :meth:`reset_heading` makes the current yaw read as the given angle.
    """

    ext_port: int

    def __init__(self, port: Union[_Port, PUMPDevice], ext_port: int = 2):
        """Gyro(port, ext_port=ExtPort.EXT2)

        Arguments:
            port (Port): Hub port of the PUMP device carrying the gyro (or the
                opened ``PUMPDevice`` itself).
            ext_port (ExtPort): Extension port the gyro is plugged into. Raises
                ``OSError`` if there is no gyro there.
        """

    def read(self) -> MaybeAwaitableEuler:
        """read() -> Tuple  -- (roll, pitch, yaw, status), degrees; yaw includes the offset."""

    def heading(self) -> MaybeAwaitableFloat:
        """heading() -> float  -- yaw in degrees (-180 .. 180], with the offset applied."""

    def reset_heading(self, angle: float = 0) -> MaybeAwaitable:
        """reset_heading(angle=0)  -- make the current heading read as ``angle``."""


IMU = Gyro
"""Alias of :class:`Gyro`."""


class FloorPro:
    """LP-FloorPro connected to a PeakHub port, speaking PUMP."""

    dev: PUMPDevice
    """The underlying generic device."""
    serial: str
    """The device's 8-character short ID."""
    line: Line
    ir_raw: IRRaw
    ir_calib: IRCalib
    pixels: Pixels
    """The strip picture stream; ``None`` with firmware that lacks it."""

    def __init__(self, port: _Port):
        """FloorPro(port)

        Arguments:
            port (Port): Port the sensor is connected to. Raises ``OSError`` if
                no device is there or it is not a FloorPro.
        """

    def color_sensor(self, ext_port: int = 1) -> ColorSensor:
        """color_sensor(ext_port=1) -> ColorSensor

        The TCS3400 on extension port 1 or 2; raises ``OSError`` if none.
        """

    def gyro(self, ext_port: int = 2) -> Gyro:
        """gyro(ext_port=2) -> Gyro  -- the gyro on extension port 1 or 2; raises ``OSError`` if none."""

    def imu(self, ext_port: int = 2) -> Gyro:
        """imu(ext_port=2) -> Gyro  -- alias of :meth:`gyro`."""

    def streams(self) -> Tuple[StreamInfo, ...]:
        """streams() -> Tuple  -- the enumerated streams ``(id, url, ext_port, state_len)``."""

    def _display_source(self) -> Tuple[PUMPDevice, int, Tuple[Optional[int], ...]]:
        """(device, stream id, matrix map) consumed by ``hub.display.device()``."""
