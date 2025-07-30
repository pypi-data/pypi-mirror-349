"""
Quick and common client imports for Pax25.
"""

import tomllib
from pathlib import Path

from . import interfaces
from .applications.application import Application
from .station import Station
from .types import Version

with open(Path(__file__).parent.parent / "pyproject.toml", "rb") as package_file:
    version = tomllib.load(package_file)["project"]["version"].split(".")
    __version__ = Version(major=version[0], minor=version[1], patch=version[2])
    del version

__all__ = ["Station", "Application", "interfaces"]
