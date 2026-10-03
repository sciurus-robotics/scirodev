"""sciro.canbus -- the PeakHub CAN connectors (beta).

Classic CAN (11/29-bit identifiers, up to 8 data bytes) on CAN connector 1 or 2.
Both transceivers are powered while a program holds a ``CAN`` object and are
switched off when the program ends.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple, Union

if TYPE_CHECKING:
    from pybricks._common import MaybeAwaitable

    from ._common import MaybeAwaitableFrame

Frame = Tuple[int, bytes, bool]
"""A received frame: ``(id, data, extended)``."""


class CAN:
    """One of the hub's CAN connectors."""

    def __init__(self, bus: int, bitrate: int = 500000):
        """CAN(bus, bitrate=500000)

        Arguments:
            bus (int): Connector number, 1 or 2.
            bitrate (int): Bits per second: 125000, 250000, 500000 or 1000000.
                Raises ``OSError`` (``ENOTSUP``) on a board whose CAN
                transceivers must stay off.
        """

    def bitrate(self, bitrate: Optional[int] = None) -> Optional[int]:
        """bitrate() -> int
        bitrate(bitrate)

        Gets or sets the bit rate. Setting it restarts the controller: frames
        waiting to be sent are dropped, received frames are kept.
        """

    def send(self, id: int, data: bytes = b"", extended: bool = False, timeout: Optional[int] = 100) -> MaybeAwaitable:
        """send(id, data=b"", extended=False, timeout=100)

        Queues one frame. Waits up to ``timeout`` ms for room in the transmit
        queue (it only fills when nobody on the bus acknowledges) and raises
        ``OSError`` (``ETIMEDOUT``) after that.

        Arguments:
            id (int): Identifier, 11 bits or 29 bits with ``extended=True``.
            data (bytes): 0 to 8 bytes.
            extended (bool): Use a 29-bit identifier.
            timeout (int): Milliseconds, ``None`` to wait forever.
        """

    def recv(self, timeout: Optional[int] = 1000) -> Optional[MaybeAwaitableFrame]:
        """recv(timeout=1000) -> Tuple[int, bytes, bool] | None

        Takes the oldest received frame as ``(id, data, extended)``, or ``None``
        when nothing arrived within ``timeout`` ms (``None`` = wait forever,
        ``0`` = just poll). Under multitasking ``await`` the result; it is then
        never ``None`` at the call site, so narrow the type (e.g. ``assert``).
        """

    def pending(self) -> int:
        """pending() -> int

        Number of received frames waiting (up to 32 are queued; beyond that,
        frames are counted as lost).
        """

    def clear(self) -> None:
        """clear()

        Drops the queued received frames and zeroes the counters.
        """

    def stats(self) -> Dict[str, Union[int, bool]]:
        """stats() -> Dict

        Counters and controller state: ``tx_queued``, ``tx_done`` (acknowledged
        on the bus), ``rx``, ``rx_lost``, ``bus_off_count``, ``tec``, ``rec``
        (CAN error counters), ``lec`` (last error code, 0 none, 1 stuff, 2 form,
        3 ack, 4 bit1, 5 bit0, 6 crc, 7 unchanged), ``warning``, ``passive``,
        ``bus_off``.
        """
