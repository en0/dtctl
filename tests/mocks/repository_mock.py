from typing import override

from dflib.error import (
    ConfigSetNotFoundError,
    FileAlreadyExistsError,
    FileNotFoundError,
    OperationFailedError,
)
from dflib.typing import (
    FilterPredicate,
    IDENTITY_T,
    IRepository,
    MODEL_T,
)


class RepositoryMock(IRepository[MODEL_T, IDENTITY_T]):

    @override
    def save(self, entity: MODEL_T) -> MODEL_T:
        self.storage[getattr(entity, "id")] = entity
        return entity

    @override
    def update(self, entity: MODEL_T) -> MODEL_T:
        self.storage[getattr(entity, "id")] = entity
        return entity

    @override
    def delete(self, id: IDENTITY_T) -> None:
        self.storage.pop(id, None)

    @override
    def find_by_id(self, ident: IDENTITY_T) -> MODEL_T:
        return self.storage.get(ident)

    @override
    def find_all(self) -> list[MODEL_T]:
        return list(self.storage.values())

    @override
    def find(self, filter: FilterPredicate) -> list[MODEL_T]:
        ## TODO: This needs to get he query builder and pass it into the filter function.
        #query = filter(self.get_query_builder())
        ## TODO Implement the Visitor... also rename that to mapper.
        query_mapper = DictQueryMapper()
        query.accept(sql_query_vistor)
        return query.apply(self.storage)

    def __init__(self) -> None:
        self.storage: dict[IDENTITY_T, MODEL_T] = {}
