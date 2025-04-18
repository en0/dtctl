"""Domain Models for dflib"""


from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass
class ConfigSetEntry:
    """
    Represents an entry within a configuration set.

    Attributes:
        id (UUID): Unique identifier for the configuration set entry.
        name (Path): Path to the configuration file.
    """
    id: UUID
    name: Path


@dataclass
class ConfigSet:
    """
    Represents a collection of configuration files.

    Attributes:
        name (str): The name of the configuration set.
        files (list[ConfigSetEntry]): A list of `ConfigSetEntry` objects representing the files
                                      within the set.
    """
    name: str
    files: list[ConfigSetEntry]

