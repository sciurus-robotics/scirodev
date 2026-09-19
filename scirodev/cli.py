"""`scirodev` command line: pybricksdev's CLI (run, download, flash, ...) under
our name, so one tool covers PeakHub as well. PeakHub-specific commands can be
added here later; everything else is forwarded unchanged.
"""

import sys


def main() -> None:
    from pybricksdev.cli import main as pybricksdev_main

    sys.argv[0] = "scirodev"
    pybricksdev_main()


if __name__ == "__main__":
    main()
