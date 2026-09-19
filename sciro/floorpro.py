"""sciro.floorpro -- the LP-FloorPro line sensor over PUMP (PeakHub).

Stub for the frozen module of the same name. Every reading method returns the
value directly, or an awaitable under multitasking.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from pybricks._common import MaybeAwaitable, MaybeAwaitableFloat

    from ._common import (
        MaybeAwaitableEuler,
        MaybeAwaitableInts,
        MaybeAwaitableIRCalib,
        MaybeAwaitableLine,
        MaybeAwaitablePixels,
        MaybeAwaitableRGBC,
    )

from .iodevices import PUMPDevice, StreamInfo
from .parameters import Port as _Port


class _Stream:
    dev: PUMPDevice
    id: int

    def subscribe(self, mode: int, rate: int = 0) -> MaybeAwaitable:
        """subscribe(mode, rate=0)  -- see :meth:`PUMPDevice.subscribe`."""

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
    :meth:`sciro.hubs.PeakHub.display.device`.
    """

    def read(self) -> MaybeAwaitablePixels:
        """read() -> Tuple[Tuple[int, int, int], ...]  -- 18 RGB triplets, 0 .. 255."""

    def oneshot(self) -> MaybeAwaitablePixels:
        """oneshot() -> Tuple  -- request one frame and return it."""


class ColorSensor(_Stream):
    """TCS3400 on an extension port: raw R, G, B, C at device resolution.

    Every sample is tagged with the settings it was measured under, so a read
    after a settings change waits for the first sample taken with the new
    settings.
    """

    def read(self) -> MaybeAwaitableRGBC:
        """read() -> Tuple[int, int, int, int, int]  -- (red, green, blue, clear, status)."""

    def settings(self) -> Tuple[int, int, int]:
        """settings() -> Tuple[int, int, int]  -- (led_percent, gain_x, atime) in effect."""

    def set_light(self, percent: int) -> MaybeAwaitable:
        """set_light(percent)  -- illumination LED duty, 0 .. 100."""

    def set_gain(self, gain_x: int) -> MaybeAwaitable:
        """set_gain(gain_x)  -- analog gain: 1, 4, 16 or 64."""

    def set_integration(self, atime: int) -> MaybeAwaitable:
        """set_integration(atime)  -- TCS3400 ATIME register 0 .. 255: (256 - atime) * 2.78 ms."""


class IMU(_Stream):
    """BNO086 on an extension port: roll, pitch, yaw in degrees.

    The heading offset lives on the hub: :meth:`reset_heading` makes the current
    yaw read as the given angle.
    """

    def read(self) -> MaybeAwaitableEuler:
        """read() -> Tuple  -- (roll, pitch, yaw, status), degrees; yaw includes the offset."""

    def heading(self) -> MaybeAwaitableFloat:
        """heading() -> float  -- yaw in degrees (-180 .. 180], with the offset applied."""

    def reset_heading(self, angle: float = 0) -> MaybeAwaitable:
        """reset_heading(angle=0)  -- make the current heading read as ``angle``."""


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

    def imu(self, ext_port: int = 2) -> IMU:
        """imu(ext_port=2) -> IMU  -- the BNO086 on extension port 1 or 2; raises ``OSError`` if none."""

    def streams(self) -> Tuple[StreamInfo, ...]:
        """streams() -> Tuple  -- the enumerated streams ``(id, url, ext_port, state_len)``."""

    def _display_source(self) -> Tuple[PUMPDevice, int, Tuple[Optional[int], ...]]:
        """(device, stream id, matrix map) consumed by ``hub.display.device()``."""
