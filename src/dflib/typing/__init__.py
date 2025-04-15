"""
typing.py

This module contains abstract base classes (ABCs) and interface definitions
for the dflib library. These interfaces define the contracts that various
components of the library must adhere to, ensuring consistency and facilitating
extensibility.

Usage:
------
This module is intended to be used as a central location for defining interface
contracts. Implementations of these interfaces should reside in separate modules
aligned with specific functionality or storage backends.

Extendability:
--------------
New interfaces or enhancements to existing interfaces can be added to this module
as the library evolves.
"""

from .config_set_file_handler import IConfigSetFileHandler

__all__ = [
    "IConfigSetFileHandler",
]
