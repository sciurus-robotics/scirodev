"""Stubs for ``sciro.robotics`` (PeakHub firmware) -- control helpers.
EXPERIMENTAL: the API may still change between releases.
"""

from __future__ import annotations

from typing import Optional, Tuple

from pybricks.parameters import Number, Stop
from pybricks._common import MaybeAwaitable

from pybricks import _common
from pybricks.robotics import DriveBase as _DriveBase
from pybricks.tools import StopWatch

from sciro.tools import Logger, RingBuffer


class Control(_common.Control):
    """A drivebase / motor controller, with its built-in logger exposed."""

    log: Logger


class DriveBase(_DriveBase):
    """``pybricks.robotics.DriveBase`` (the same class on the hub). The stub
    adds the ``log`` on ``heading_control`` / ``distance_control`` and the
    PeakHub extensions of :meth:`straight`."""

    heading_control: Control  # type: ignore[assignment]
    distance_control: Control  # type: ignore[assignment]

    def straight(  # type: ignore[override]
        self,
        distance: Number,
        then: Stop = Stop.HOLD,
        wait: bool = True,
        speed: Optional[Number] = None,
        heading: Optional[Number] = None,
        exit_speed: Number = 0,
    ) -> MaybeAwaitable:
        """straight(distance, then=Stop.HOLD, wait=True, speed=None, heading=None, exit_speed=0)

        Drives straight for ``distance`` mm, as in Pybricks, with three
        PeakHub extensions (keyword use recommended):

        ``speed``: drive speed in mm/s for this move only; ``None`` uses the
        ``straight_speed`` setting.

        ``heading``: absolute heading in degrees to hold during the move
        instead of the heading at its start (the gyro heading with
        ``use_gyro(True)``, else the wheel-based one since the last
        ``reset()``). Any value is accepted: the nearest whole-turn
        equivalent of the current heading is targeted, so ``heading=90``
        while the internal heading reads 450 corrects by 0 degrees, never by
        a full turn. ``None`` keeps the Pybricks behavior.

        ``exit_speed``: speed in mm/s the robot has when it reaches the
        target; it keeps driving at that speed until the next command, so the
        next ``straight()`` (or ``drive()``) blends in without a stop. Implies
        ``then=Stop.NONE``; any other explicit ``then`` raises ``ValueError``.
        Clamped to the move's drive speed. ``0`` (default) stops or holds as
        ``then`` says. ``then=Stop.NONE`` without ``exit_speed`` keeps the
        upstream meaning: continue at the drive speed.
        """

    def heading_target(self, angle: Optional[Number] = None) -> Optional[float]:
        """heading_target(angle) / heading_target() -> float

        Steers a running :meth:`straight` (PeakHub): replaces the heading
        setpoint without touching the distance trajectory (position, speed,
        exit speed and end condition stay). Absolute heading in degrees,
        float, same frame and nearest-whole-turn rule as ``straight(heading=)``.
        The heading controller branches off its current reference on a new
        trajectory, so small steps (the usual < 1 degree per 10 ms) are smooth
        and large ones are limited by the ``turn_rate`` / ``turn_acceleration``
        settings. Without an argument returns the current heading target.

        Typical use, a line follower as a setpoint generator::

            db.straight(dist, speed=v, exit_speed=e, heading=course, wait=False)
            while not db.done():
                data = await floor.all_sensor_data()
                db.heading_target(course + K * data[0])
                await wait(10)

        Raises ``OSError`` when no ``straight()`` is running (``drive()``,
        ``turn()``, ``curve()``, ``arc()`` and an idle drivebase are not
        steerable).
        """


class PIDController:
    """Discrete PID controller: ``output = kp*e + ki*integral(e) + kd*de/dt``.

    ``ki = kd = 0`` gives a plain P or PD controller. ``integral_limit`` clamps
    the I term (anti-windup), ``output_limit`` the total output; ``None`` means
    unlimited. A gap between updates longer than ``reset_after`` milliseconds
    restarts the controller (a new movement); ``None`` never. ``stopwatch``
    is the time source (default: an own ``StopWatch``); ``log`` a
    :class:`RingBuffer` with :attr:`LOG_FIELDS` (see :meth:`make_log`).
    """

    LOG_FIELDS: Tuple[Tuple[str, str], ...]
    """``t_ms, dt, error, p, i, d, output`` -- the row layout of the log."""

    kp: float
    ki: float
    kd: float
    integral_limit: Optional[float]
    output_limit: Optional[float]
    reset_after: Optional[int]
    stopwatch: StopWatch
    log: Optional[RingBuffer]
    name: str
    output: float
    """The last output."""
    integral: float

    def __init__(
        self,
        kp: float,
        ki: float = 0.0,
        kd: float = 0.0,
        integral_limit: Optional[float] = None,
        output_limit: Optional[float] = None,
        reset_after: Optional[int] = 100,
        stopwatch: Optional[StopWatch] = None,
        log: Optional[RingBuffer] = None,
        name: str = "PID",
    ) -> None: ...

    def make_log(self, seconds: float, rate: int = 100) -> RingBuffer:
        """Attach and return a RingBuffer for ``seconds`` of updates at ``rate`` Hz."""

    def reset(self) -> None:
        """Forget the integral, the last error and the last update time."""

    def update(self, error: float, derivative: Optional[float] = None, p_limit: Optional[float] = None) -> float:
        """One controller step; returns the output.

        ``error`` is setpoint minus measurement. ``derivative`` is d(error)/dt
        when measured (e.g. minus the gyro rate for a heading error); ``None``
        differentiates the error numerically. ``p_limit`` clamps the P term for
        this step only, e.g. a braking profile that leaves the D term free to
        damp.
        """
