"""Domain Models for dflib"""

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass
class ConfigSetEntry:
    id: UUID
    name: Path


@dataclass
class ConfigSet:
    name: str
    files: ConfigSetEntry

