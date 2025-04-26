from typing import override

from dflib.error import DuplicateEntityError, EntityNotFoundError
from dflib.model import ConfigSet
from dflib.typing import FilterPredicate, IRepository


class ConfigSetRepositoryMock(IRepository[ConfigSet, str]):

    @override
    def save(self, entity: ConfigSet) -> ConfigSet:
        if entity.name in self._datastore:
            raise DuplicateEntityError(entity.name)
        self._datastore[entity.name] = entity
        return entity

    @override
    def update(self, entity: ConfigSet) -> ConfigSet:
        if entity.name not in self._datastore:
            raise EntityNotFoundError(entity.name)
        self._datastore[entity.name] = entity
        return entity

    @override
    def delete(self, ident: str) -> None:
        if ident not in self._datastore:
            raise EntityNotFoundError(ident)
        del self._datastore[ident]

    @override
    def find_by_id(self, ident: str) -> ConfigSet:
        if ident not in self._datastore:
            raise EntityNotFoundError(ident)
        return self._datastore[ident]

    @override
    def find_all(self) -> list[ConfigSet]:
        return list(self._datastore.values())

    @override
    def find(self, filter: FilterPredicate) -> list[ConfigSet]:
        raise NotImplementedError()

    def __init__(self):
        self._datastore: dict[str, ConfigSet] = {}
