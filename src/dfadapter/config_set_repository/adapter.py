from configparser import ConfigParser, DuplicateSectionError
from logging import getLogger
from pathlib import Path
from typing import override
from uuid import UUID

from pyioc3.autowire import bind

from dflib.error import DuplicateEntityError, EntityNotFoundError
from dflib.model import ConfigSet, ConfigSetEntry
from dflib.typing import FilterPredicate, IRepository

from .config import LocalConfigSetRepositoryConfig

logger = getLogger(__name__)


@bind(IRepository[ConfigSet, str], scope="SINGLETON")
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
        try:
            self._catalog.add_section(entity.name)
            for file in entity.files:
                self._catalog[entity.name][str(file.name)] = str(file.id)
            self._write_catalog()

        except DuplicateSectionError:
            raise DuplicateEntityError(entity.name)

        return entity

    @override
    def update(self, entity: ConfigSet) -> ConfigSet:
        try:
            del self._catalog[entity.name]
            return self.save(entity)
        except KeyError:
            raise EntityNotFoundError(entity.name)

    @override
    def delete(self, ident: str) -> None:
        try:
            del self._catalog[ident]
            self._write_catalog()
        except KeyError:
            raise EntityNotFoundError(ident)

    @override
    def find_by_id(self, ident: str) -> ConfigSet:
        try:
            cs = ConfigSet(ident, [])
            for name, uid in self._catalog[ident].items():
                entry = ConfigSetEntry(UUID(uid), Path(name))
                cs.files.append(entry)
            return cs
        except KeyError:
            raise EntityNotFoundError(ident)

    @override
    def find_all(self) -> list[ConfigSet]:
        return [self.find_by_id(n) for n in self._catalog.sections()]

    @override
    def find(self, filter: FilterPredicate) -> list[ConfigSet]:
        raise NotImplementedError()

    def _write_catalog(self) -> None:
        self._catalog_path.parent.mkdir(parents=True, exist_ok=True)
        with self._catalog_path.open("w") as fp:
            self._catalog.write(fp)

    def __init__(self, config: LocalConfigSetRepositoryConfig):
        self._catalog_path: Path = config.catalog_path
        self._catalog: ConfigParser = ConfigParser()
        if self._catalog_path.exists():
            with self._catalog_path.open("r") as fp:
                self._catalog.read_file(fp)
