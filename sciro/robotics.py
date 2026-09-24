"""Stubs for ``sciro.robotics`` (PeakHub firmware) -- control helpers.
EXPERIMENTAL: the API may still change between releases.
"""

from __future__ import annotations

from typing import Optional, Tuple

from pybricks import _common
from pybricks.robotics import DriveBase as _DriveBase
from pybricks.tools import StopWatch

from sciro.tools import Logger, RingBuffer


class Control(_common.Control):
    """A drivebase / motor controller, with its built-in logger exposed."""

    log: Logger


class DriveBase(_DriveBase):
    """``pybricks.robotics.DriveBase`` (the same class on the hub); the stub
    adds the ``log`` on ``heading_control`` / ``distance_control``."""

    heading_control: Control  # type: ignore[assignment]
    distance_control: Control  # type: ignore[assignment]


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
