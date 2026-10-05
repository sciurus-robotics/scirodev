"""`scirodev` command line.

One tool for Sciurus Robotics hubs (PeakHub so far). It is built on
pybricksdev: pybricksdev's own tools (run, compile, flash, ...) are offered
unchanged, next to the tools that only exist for sciro hubs (rename).
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from . import __version__

DESCRIPTION = """\
Command line tool for Sciurus Robotics hubs (PeakHub).

Built on pybricksdev. Tools marked [pybricksdev] are pybricksdev's own,
unchanged, and work with any hub running Pybricks firmware. The other tools
are extensions for sciro hubs.
"""

EPILOG = """\
Run `%(prog)s <tool> --help` for tool-specific arguments.

Examples:
  %(prog)s run ble --name Peak-BYN9 program.py
  %(prog)s rename ble MyRobot --name Peak-BYN9
"""

# pybricksdev tools to offer, by class name. Looked up by name so a pybricksdev
# release that adds or drops one does not break us.
PYBRICKSDEV_TOOLS = ("Compile", "Run", "Flash", "DFU", "OAD", "LWP3", "Udev")


def _pybricksdev_version() -> str:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("pybricksdev")
    except PackageNotFoundError:
        return "?"


def build_parser() -> tuple[argparse.ArgumentParser, argparse._SubParsersAction]:
    import pybricksdev.cli as pbcli

    from .rename import Rename

    parser = argparse.ArgumentParser(
        prog="scirodev",
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"scirodev v{__version__} (pybricksdev v{_pybricksdev_version()})",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug logging")

    subparsers = parser.add_subparsers(metavar="<tool>", dest="tool", help="the tool to use")

    # Our own tools first.
    for tool in (Rename(),):
        tool.add_parser(subparsers)
    own = len(subparsers._choices_actions)

    for name in PYBRICKSDEV_TOOLS:
        cls = getattr(pbcli, name, None)
        if cls is not None:
            cls().add_parser(subparsers)

    # Mark what comes from pybricksdev in the tool list.
    for action in subparsers._choices_actions[own:]:
        action.help = f"{action.help or ''} [pybricksdev]".strip()

    return parser, subparsers


def pairing_hint(error: str) -> str | None:
    """Plain words for the Bluetooth errors a PIN-protected hub can cause."""
    e = error.lower()
    if "peer removed pairing information" in e:
        return (
            "This computer was paired with the hub, but the hub no longer knows it\n"
            "(its PIN was set or changed). Make the computer forget the hub in its\n"
            "Bluetooth settings, then run the command again and enter the hub's PIN."
        )
    if "authentication" in e or "encryption is insufficient" in e or "pairing" in e:
        return (
            "The hub is protected with a PIN. Enter it in the dialog of your operating\n"
            "system when it appears; if the command gave up meanwhile, run it again.\n"
            "After 3 wrong PINs the hub refuses new computers until its Bluetooth\n"
            "button is switched off and on."
        )
    return None


def main() -> None:
    if sys.platform == "win32":
        # Same workaround as pybricksdev: bad side effects of pythoncom.
        try:
            from bleak_winrt._winrt import MTA, init_apartment
        except ImportError:
            from winrt._winrt import MTA, init_apartment

        init_apartment(MTA)

    parser, subparsers = build_parser()

    try:
        import argcomplete

        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
        level=logging.DEBUG if args.debug else logging.WARNING,
    )

    if not args.tool:
        parser.error(f'Missing name of tool: {"|".join(subparsers.choices.keys())}')

    try:
        result = asyncio.run(subparsers.choices[args.tool].tool.run(args))
    except Exception as e:
        hint = pairing_hint(str(e))
        if hint is None or args.debug:
            raise
        print(f"error: {e}\n\n{hint}", file=sys.stderr)
        sys.exit(1)
    if isinstance(result, int) and result:
        sys.exit(result)


if __name__ == "__main__":
    main()
