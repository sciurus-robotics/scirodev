"""`scirodev rename`: give a PeakHub a name of its own.

The name is what the hub advertises over Bluetooth (so `scirodev run ble
--name <name>` finds exactly this hub), what `hub.system.name()` returns, and
it is stored on the hub across power cycles and firmware updates.

Over USB the hub takes the name at once. Over Bluetooth, where anybody in
range could send the command, the hub spells the new name on its display,
shows a `?` and applies it only when the centre button is pressed (any other
button, or 10 s without one, rejects it).
"""

from __future__ import annotations

import argparse
import asyncio
import sys

# PeakHub extension of the Pybricks command set (PBIO_PYBRICKS_COMMAND_SET_HUB_NAME).
SET_HUB_NAME = 0xA0
NAME_MAX = 16


def check_name(name: str) -> str:
    if name == "":
        return name
    if len(name) > NAME_MAX:
        raise argparse.ArgumentTypeError(f"at most {NAME_MAX} characters")
    if any(not (0x20 <= ord(c) <= 0x7E) for c in name):
        raise argparse.ArgumentTypeError("printable ASCII characters only")
    if name != name.strip():
        raise argparse.ArgumentTypeError("no leading or trailing spaces")
    return name


def parse(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="scirodev rename",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("conntype", choices=["ble", "usb"], help="how to reach the hub")
    p.add_argument(
        "new_name",
        type=check_name,
        nargs="?",
        help=f"the new name: 1 to {NAME_MAX} printable ASCII characters",
    )
    p.add_argument("--default", action="store_true", help="go back to the default name (Peak-XXXX)")
    p.add_argument("-n", "--name", help="current name of the hub to rename (ble; default: first hub found)")
    args = p.parse_args(argv)
    if args.default == (args.new_name is not None):
        p.error("give either a new name or --default")
    if args.default:
        args.new_name = ""
    elif args.new_name == "":
        p.error("the name must not be empty (use --default for the default name)")
    return args


async def rename(args: argparse.Namespace) -> int:
    from pybricksdev.ble.pybricks import PYBRICKS_COMMAND_EVENT_UUID

    if args.conntype == "ble":
        from pybricksdev.ble import find_device
        from pybricksdev.connections.pybricks import PybricksHubBLE

        print(f"Searching for {args.name or 'any hub with Pybricks service'}...")
        hub = PybricksHubBLE(await find_device(args.name))
    else:
        from usb.core import find as find_usb

        from pybricksdev.connections.pybricks import PybricksHubUSB
        from pybricksdev.usb import LEGO_USB_VID

        device = find_usb(custom_match=lambda d: d.idVendor == LEGO_USB_VID and d.product.endswith("Pybricks"))
        if device is None:
            print("Pybricks Hub not found.", file=sys.stderr)
            return 1
        hub = PybricksHubUSB(device)

    shown = args.new_name or "the default name"
    await hub.connect()
    try:
        await hub.write_gatt_char(
            PYBRICKS_COMMAND_EVENT_UUID,
            bytes([SET_HUB_NAME]) + args.new_name.encode("ascii"),
            True,
        )
        if args.conntype == "ble":
            print(f"The hub now shows the new name ({shown}) and then '?'.")
            print("Press the centre button on the hub to accept. Any other button, or 10 s, rejects.")
            # Stay connected while the user decides, so nobody else can slip in.
            await asyncio.sleep(len(args.new_name) * 0.6 + 10.5)
            print("Done. If accepted, the hub advertises under the new name from the next connection on.")
        else:
            print(f"Renamed to {shown}.")
    finally:
        await hub.disconnect()
    return 0


def main(argv: list[str]) -> None:
    args = parse(argv)
    sys.exit(asyncio.run(rename(args)))
