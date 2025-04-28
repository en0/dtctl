from logging import getLogger
from pathlib import Path
from typing import override

from dflib.model import ConfigSet
from dflib.typing import FilterPredicate, IRepository

from .config import LocalConfigSetRepositoryConfig

logger = getLogger(__name__)


class LocalConfigSetRepository(IRepository[ConfigSet, str]):
    """A local filesystem implementation of the IRepository interface for managing ConfigSets.

    This class provides a concrete implementation of the IRepository interface, specifically
    designed for handling ConfigSets. It facilitates the storage and retrieval of ConfigSet metadata
    within a local filesystem, using an INI file format to catalog the association between file
    paths and their unique identifiers.

    Each ConfigSet is represented as a section in the INI file, with the section name prefixed by
    'ConfigSet:'. Within each section, file paths are mapped to their corresponding UUIDs, allowing
    for efficient lookup and management of files associated with a particular ConfigSet.

    Example INI file structure:
    [ConfigSet:MyConfigSetName]
    /some/file/path = uuid-of-file-identity

    Multiple files within a ConfigSet are listed under the same section, ensuring all related
    files are grouped together.

    The location of the catalog file is determined by the 'catalogPath' configuration key within
    the 'ConfigSetRepository.LocalFS' section of the host configuration.
    """

    @override
    def save(self, entity: ConfigSet) -> ConfigSet:
        raise NotImplementedError()

    @override
    def update(self, entity: ConfigSet) -> ConfigSet:
        raise NotImplementedError()

    @override
    def delete(self, ident: str) -> None:
        raise NotImplementedError()

    @override
    def find_by_id(self, ident: str) -> ConfigSet:
        raise NotImplementedError()

    @override
    def find_all(self) -> list[ConfigSet]:
        raise NotImplementedError()

    @override
    def find(self, filter: FilterPredicate) -> list[ConfigSet]:
        raise NotImplementedError()

    def __init__(self, config: LocalConfigSetRepositoryConfig):
        self.file_store_dir: Path = config.catalog_path
