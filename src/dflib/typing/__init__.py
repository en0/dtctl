"""
Typing module.

This module contains abstract base classes (ABCs) and interface definitions
for the dflib library. These interfaces define the contracts that various
components of the library must adhere to, ensuring consistency and facilitating
extensibility.

Usage:
------
This module is intended to be used as a central location for defining interface
contracts. Implementations of these interfaces should reside in separate modules
aligned with specific functionality or storage backends.
"""

from .config_set_file_handler import IConfigSetFileHandler
from .repository import (
    IDENTITY_T,
    MODEL_T,
    FilterPredicate,
    IFilterVisitor,
    IQueryBuilder,
    IRepository,
)

__all__ = [
    "FilterPredicate",
    "IConfigSetFileHandler",
    "IDENTITY_T",
    "IQueryBuilder",
    "IFilterVisitor",
    "IRepository",
    "MODEL_T",
]
