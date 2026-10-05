"""scirodev -- tooling for Sciurus Robotics hubs on top of pybricksdev, and the `sciro` API stubs."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("scirodev")
except PackageNotFoundError:  # running from a source tree that is not installed
    __version__ = "0+unknown"
