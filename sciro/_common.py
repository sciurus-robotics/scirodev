"""Typing helpers for the sciro stubs, in the style of ``pybricks._common``:
a value that is returned directly, or awaitable under multitasking. The
upstream ``MaybeAwaitableTuple[T]`` is a 1-tuple, so fixed-shape results get
their own classes here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from typing import Awaitable

    _Line = Tuple[float, float, float, float, int, bool]
    _Ints = Tuple[int, ...]
    _IRCalib = Tuple[Tuple[int, ...], Tuple[int, ...], int, int]
    _RGBC = Tuple[int, int, int, int, int]
    _Euler = Tuple[float, float, float, int]
    _StateData = Tuple[bytes, bytes]
    _RGB = Tuple[int, int, int]
    _Calibration = Tuple[Tuple[int, int, int, int], Tuple[int, int, int, int], Tuple[int, int, int], bool, bool, int]
    _Pixels = Tuple[_RGB, ...]

    class MaybeAwaitableLine(_Line, Awaitable[_Line]): ...

    class MaybeAwaitableInts(_Ints, Awaitable[_Ints]): ...

    class MaybeAwaitableIRCalib(_IRCalib, Awaitable[_IRCalib]): ...

    class MaybeAwaitableRGBC(_RGBC, Awaitable[_RGBC]): ...

    class MaybeAwaitableEuler(_Euler, Awaitable[_Euler]): ...

    class MaybeAwaitableStateData(_StateData, Awaitable[_StateData]): ...

    class MaybeAwaitablePixels(_Pixels, Awaitable[_Pixels]): ...

    class MaybeAwaitableRGB8(_RGB, Awaitable[_RGB]): ...

    class MaybeAwaitableCalibration(_Calibration, Awaitable[_Calibration]): ...

    class MaybeAwaitableStr(str, Awaitable[str]): ...
