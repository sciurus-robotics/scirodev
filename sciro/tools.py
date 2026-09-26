"""Stubs for ``sciro.tools`` (PeakHub firmware) -- recording and publishing
helpers. EXPERIMENTAL: the API may still change between releases.
"""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

if TYPE_CHECKING:
    from pybricks._common import MaybeAwaitableTuple
else:
    # Upstream defines this only for type checkers; runtime importers of the
    # stubs (the docs build) need a value. Annotations are strings here
    # (from __future__ import annotations), so a placeholder suffices.
    MaybeAwaitableTuple = None


def multitask(*coroutines: Awaitable[Any], race: bool = False) -> MaybeAwaitableTuple:
    """multitask(coroutine1, coroutine2, ..., race=False) -> Tuple

    ``pybricks.tools.multitask`` (the same function on the hub), typed to
    accept any awaitable.

    The upstream stub asks for ``Coroutine``, which every *maybe-awaitable*
    hub method fails to satisfy for a type checker: ``motor.run_angle(...)``,
    ``db.straight(...)`` or ``sensor.read()`` are declared as awaitables, not
    as coroutines, because they return a plain value when called outside
    ``run_task``. Importing ``multitask`` (and :func:`run_task`) from
    ``sciro.tools`` instead of ``pybricks.tools`` removes those warnings::

        from sciro.tools import multitask, run_task

        async def main():
            await multitask(db.straight(500), log.record(db.state), race=True)

        run_task(main())
    """


def run_task(coroutine: Optional[Awaitable[Any]] = None) -> Optional[bool]:
    """run_task(coroutine) -> bool | None

    ``pybricks.tools.run_task`` (the same function on the hub), typed to
    accept any awaitable; see :func:`multitask`. Without an argument it
    returns whether the run loop is active.
    """


class RingBuffer:
    """Fixed-size recorder of rows with a fixed binary layout, kept in RAM.

    ``fields`` are ``(name, format)`` pairs with ``struct`` formats (``"I"``
    unsigned 32 bit, ``"i"`` signed, ``"f"`` float, ``"h"`` 16 bit, ``"B"``
    byte, ...); ``capacity`` rows are kept, older rows are overwritten.
    RAM used = capacity * row size (100 Hz * 30 s * 7 floats = 84 KB).
    """

    fields: Tuple[Tuple[str, str], ...]
    names: Tuple[str, ...]
    format: str
    row_size: int
    capacity: int
    name: Optional[str]
    count: int
    """Rows appended since the last clear (not capped at capacity)."""

    def __init__(self, fields: Iterable[Sequence[str]], capacity: int, name: Optional[str] = None) -> None: ...

    def __len__(self) -> int:
        """Rows currently kept (at most ``capacity``)."""

    def __getitem__(self, idx: int) -> Tuple[float | int, ...]:
        """Row ``idx`` as a tuple; 0 is the oldest kept row, -1 the newest."""

    def __iter__(self) -> Iterator[Tuple[float | int, ...]]:
        """Rows, oldest first."""

    def clear(self) -> None: ...

    def append(self, *values: float | int) -> None:
        """Append one row; values in field order."""

    def record(self, source: Callable[[], Sequence[float | int]], period: int = 10) -> Awaitable[None]:
        """Coroutine: append ``source()`` every ``period`` ms until cancelled.

        Run it next to the movement, e.g.
        ``await multitask(drive(), log.record(db.state), race=True)``.
        """

    def publish(self, path: Optional[str] = None, decimals: int = 3) -> None:
        """Print the rows as CSV (``#`` header comments, then the names).

        With ``path`` the block is wrapped in the pybricksdev file markers
        (``_file_begin_ <path>`` ... ``_file_end_``): ``scirodev run`` writes it
        to that file, relative to the folder of the running script, instead of
        the terminal. Expect on the order of 1000 rows per few seconds over BLE.
        """


class Logger:
    """The built-in pbio logger of a controller (``DriveBase.heading_control.log``,
    ``DriveBase.distance_control.log``, ``Motor.log``): rows are written by
    the firmware's 5 ms control loop while the controller is active, into a
    fixed buffer (not a ring) allocated by :meth:`start`.

    Controller columns: ``t_ms, traj_ms, position, speed, status, torque,
    ref_position, ref_speed, est_position, est_speed, p, i, d, position_c``
    (``position_c`` = position in 0.01 units, PeakHub; position in
    the controller's units: mm or deg; torque in uNm; status bits: actuation
    0..1, stalled 2, on target 3, integration paused 4).
    Servo (Motor) columns: ``t_ms, time_ms, angle, speed, status, voltage_mv,
    est_angle, est_speed, torque_fb, torque_ff, observer_mv``.
    """

    def start(self, duration: int, down_sample: int = 1) -> None:
        """Allocate and start: ``duration`` ms, one row every
        ``5 * down_sample`` ms. RAM = rows * 52 bytes (controller), so 30 s at
        ``down_sample=2`` (100 Hz) is 156 KB; prefer 10 (20 Hz) for long runs.
        """

    def stop(self) -> None: ...

    def save(self, path: Optional[str] = None) -> None:
        """Upstream: print the rows framed with ``PB_OF:<path>`` / ``PB_EOF``,
        no header. Kept unchanged."""

    def publish(self, path: Optional[str] = None, names: Optional[str] = None) -> None:
        """PeakHub: print the rows as CSV with a header line, framed with the
        ``_file_begin_ <path>`` / ``_file_end_`` markers like
        :meth:`RingBuffer.publish`. ``names`` overrides the header
        (comma separated). Stops logging first."""
