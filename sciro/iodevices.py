"""sciro.iodevices -- PeakHub-only device classes (re-exported from
``pybricks.iodevices`` on the hub; declared here for the IDE).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple, Union

if TYPE_CHECKING:
    from pybricks._common import MaybeAwaitable

    from ._common import MaybeAwaitableStateData

from .parameters import Port as _Port

# (stream id, url, ext_port, state length)
StreamInfo = Tuple[int, str, int, int]


class PUMPDevice:
    """Generic access to a PUMP device (Power UART Multiplex Protocol) on a
    PeakHub port. Streams are addressed by id (1..N); state and data are raw
    ``bytes`` decoded by the user or a convenience class such as
    :class:`sciro.pump.FloorPro`. Spec: ``PUMP-Protocol.md``.
    """

    OFF: int = 0
    """Stream-control mode: stream is silent."""
    ONESHOT: int = 1
    """Stream-control mode: one frame, then the mode self-clears to OFF."""
    ON_CHANGE: int = 2
    """Stream-control mode: a frame whenever a new sample differs."""
    PERIODIC: int = 3
    """Stream-control mode: every sample (rate 0) or at the given rate."""

    def __init__(self, port: _Port):
        """PUMPDevice(port)

        Arguments:
            port (Port): Port the device is connected to. Raises ``OSError``
                (``ENODEV``) if no PUMP device has completed its handshake there
                within a few seconds.
        """

    def info(self) -> Dict[str, Union[str, Tuple[StreamInfo, ...]]]:
        """info() -> Dict

        Returns:
            ``{"url": str, "serial": str, "streams": ((id, url, ext_port, state_len), ...)}``
        """

    def stats(self) -> Dict[str, Union[int, Tuple[Tuple[int, int, int], ...]]]:
        """stats() -> Dict

        Link counters since the session started, for load tests and diagnostics:
        ``{"frames": good frames received, "crc_errors", "cobs_errors",
        "short_frames", "overflows", "streams": ((id, frames, gaps), ...)}``
        where ``gaps`` counts frames of that stream the hub never received.
        """

    def state(self, stream: int) -> Optional[bytes]:
        """state(stream) -> bytes | None

        The last state prefix echoed by the stream (first two bytes are the
        stream-control word: mode, rate), or ``None`` if none was received yet.
        """

    def read(self, stream: int) -> MaybeAwaitableStateData:
        """read(stream) -> Tuple[bytes, bytes]

        Waits for a frame measured under the currently requested settings and
        returns ``(state, data)``. Awaitable under multitasking.
        """

    def change_state(self, stream: int, state: bytes) -> MaybeAwaitable:
        """change_state(stream, state)

        Sets the stream's whole state prefix (must be exactly its length) and
        waits until the device echoes it. Raises ``OSError`` (``ETIMEDOUT``) if
        the device never acknowledges.
        """

    def subscribe(self, stream: int, mode: int, rate: int = 0) -> MaybeAwaitable:
        """subscribe(stream, mode, rate=0)

        Changes only the stream-control word (keeps the device-specific state
        bytes). ``rate`` is in Hz (1 .. 255; higher values are clamped to 255),
        0 = every sample.
        """
