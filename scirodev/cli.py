"""`scirodev` command line: pybricksdev's CLI (run, download, flash, ...) under
our name, so one tool covers PeakHub as well. PeakHub-specific commands live
here (`rename`); everything else is forwarded unchanged.
"""

import sys


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "rename":
        from .rename import main as rename_main

        rename_main(sys.argv[2:])
        return

    from pybricksdev.cli import main as pybricksdev_main

    sys.argv[0] = "scirodev"
    pybricksdev_main()


if __name__ == "__main__":
    main()
