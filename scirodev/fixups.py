"""Robustness fix-ups applied to pybricksdev at start-up.

Two things pybricksdev does not do, both measured on an Apple-silicon Mac
with a PeakHub on 2026-10-15:

1. USB connect. pybricksdev resets the USB device and then configures it
   through the same handle. A reset makes the hub re-enumerate (new USB
   address, ~50 ms), and on macOS a handle kept across that is a lottery:
   with the stock sequence 4 of 6 connects succeeded, the rest failed with
   "[Errno 19] No such device". Google Chrome, which keeps a handle on any hub
   Pybricks Code was ever allowed to use, also re-resets the hub about one time
   in eight right after it reappears. Here the hub is looked up afresh after
   the reset, after a short settle so that such a second re-enumeration has
   passed too, and the rest of the connect is retried if the handle dies
   anyway. 100+ connects without a failure afterwards.

2. A program still running on the hub (the previous host was killed, or
   Ctrl-C'd without stopping it) makes a download fail with "Write failed:
   129" (BUSY), because pybricksdev downloads first and only then starts.
   Here the program is stopped before the download.
"""

from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger(__name__)

# Pybricks USB identity (LEGO vendor id, Pybricks product id).
PYBRICKS_VID = 0x0694
PYBRICKS_PID = 0x0009

# Let the hub re-enumerate, and let anyone else on the host who reacts to that
# (Chrome re-resets it within ~0.35 s) finish, before looking it up again.
SETTLE_S = 0.5
# Then look for it, with a fresh libusb context after the first miss, for up to
REFIND_ATTEMPTS = 60
REFIND_INTERVAL_S = 0.1
# and redo the connect this many times if the handle dies on the way.
CONNECT_ROUNDS = 3


def _patched(fn) -> bool:
    return getattr(fn, "_scirodev_patched", False)


def install_usb_connect() -> None:
    try:
        import usb.backend.libusb1 as libusb1
        import usb.core
        import usb.util
        from pybricksdev.connections.pybricks import PybricksHubUSB
    except ImportError:
        return
    original = getattr(PybricksHubUSB, "_client_connect", None)
    if original is None or _patched(original):
        return

    def gone(e: Exception) -> bool:
        # NO_DEVICE (19) / NOT_FOUND (2): the handle refers to a device that
        # has re-enumerated since; find it again.
        return isinstance(e, usb.core.USBError) and getattr(e, "errno", None) in (2, 19)

    async def refind(serial):
        backend = None  # pyusb's shared libusb context first
        last = None
        for _ in range(REFIND_ATTEMPTS):
            await asyncio.sleep(REFIND_INTERVAL_S)
            try:
                candidates = list(usb.core.find(find_all=True, idVendor=PYBRICKS_VID, idProduct=PYBRICKS_PID, backend=backend))
            except usb.core.USBError as e:
                last = e
                continue
            for device in candidates:
                try:
                    if serial is not None and device.serial_number != serial:
                        continue
                    device.set_configuration()
                    return device
                except usb.core.USBError as e:
                    last = e
                    usb.util.dispose_resources(device)
                    if backend is None:
                        # The shared context's device list can lag behind a
                        # re-enumeration (it still holds the old entry while
                        # another process keeps that open); a fresh context
                        # enumerates what is there now.
                        backend = libusb1._LibUSB(libusb1._lib)
        raise last or usb.core.USBError("Pybricks hub did not come back after the USB reset", 19, 19)

    async def _client_connect(self):
        try:
            serial = self._device.serial_number
        except usb.core.USBError:
            serial = None
        try:
            self._device.reset()
        except usb.core.USBError as e:
            logger.debug("USB reset reported %s (expected on macOS)", e)
        await asyncio.sleep(SETTLE_S)

        for round_ in range(CONNECT_ROUNDS):
            device = await refind(serial)
            self._device = device
            # The stock method with its reset and configuration already done.
            device.reset = lambda: None
            device.set_configuration = lambda *args, **kwargs: None
            try:
                return await original(self)
            except usb.core.USBError as e:
                if not gone(e) or round_ == CONNECT_ROUNDS - 1:
                    raise
                logger.debug("hub re-enumerated during connect (%s); retrying", e)
            finally:
                del device.reset
                del device.set_configuration

    _client_connect._scirodev_patched = True  # type: ignore[attr-defined]
    PybricksHubUSB._client_connect = _client_connect


def install_stop_before_run() -> None:
    try:
        from pybricksdev.connections.pybricks import PybricksHub
    except ImportError:
        return
    original = getattr(PybricksHub, "run", None)
    if original is None or _patched(original):
        return

    async def run(self, py_path=None, *args, **kwargs):
        if py_path is not None:
            # A download while a program runs is refused (BUSY); stop first.
            # Harmless when nothing runs. Errors here are left to the real run.
            try:
                await self.stop_user_program()
            except Exception as e:  # noqa: BLE001
                logger.debug("stop before run: %s", e)
        return await original(self, py_path, *args, **kwargs)

    run._scirodev_patched = True  # type: ignore[attr-defined]
    PybricksHub.run = run


LIBUSB_HINT = """\
USB needs the native libusb library, which pip does not install:
  macOS:            brew install libusb
  Debian / Ubuntu:  sudo apt install libusb-1.0-0
On an Apple-silicon Mac that has it installed, an old Intel-only
/usr/local/lib/libusb-1.0.dylib being found first causes the same error;
remove it."""


def check_usb_backend() -> str | None:
    """Returns a message if pyusb has no libusb to talk to, else None."""
    try:
        import usb.backend.libusb1 as libusb1
    except ImportError:
        return "pyusb is not installed (pip install pyusb)."
    if libusb1.get_backend() is None:
        return "libusb was not found.\n" + LIBUSB_HINT
    return None


def install_usb_backend_check() -> None:
    """Fail with a plain message instead of pyusb's NoBackendError when a USB
    connection is attempted without libusb."""
    try:
        import pybricksdev.cli as pbcli
    except ImportError:
        return
    run_cls = getattr(pbcli, "Run", None)
    original = getattr(run_cls, "run", None) if run_cls else None
    if original is None or _patched(original):
        return

    async def run(self, args):
        if getattr(args, "conntype", None) == "usb":
            problem = check_usb_backend()
            if problem:
                raise SystemExit("error: " + problem)
        return await original(self, args)

    run._scirodev_patched = True  # type: ignore[attr-defined]
    run_cls.run = run


def install() -> None:
    install_usb_backend_check()
    install_usb_connect()
    install_stop_before_run()
