from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, Callable, final, override

#from dflib.model import ConfigSet, ConfigSetEntry
from dflib.typing import IQueryBuilder, IFilterVisitor
from dflib.error import (
    DuplicateEntityError,
    EntityNotFoundError,
)
from dflib.typing import (
    FilterPredicate,
    IDENTITY_T,
    IRepository,
    MODEL_T,
)


_FilterLambda = Callable[[object], bool]


@final
class InMemoryRepoFilterVisitor(IFilterVisitor):
    """A simple in-memory filter visitor.

    This class implements a single in-memory fliter object that provides the IFilterVisitor
    interface. This class is used by the repository to apply filters from a IQueryBuilder

    Note: This class is a unit test mock.
    """

    @override
    def visitEquals(self, field: str, value: str) -> None:
        filt1 = self.filter
        filt2: _FilterLambda = lambda r: getattr(r, field) == value
        self.filter = lambda o: filt1(o) and filt2(o)

    def execute(self, records: Iterable[Any]) -> list[Any]:
        return list(filter(self.filter, records))

    def __init__(self) -> None:
        self.filter: _FilterLambda = lambda o: True


class RepositoryMock(IRepository[MODEL_T, IDENTITY_T]):
    """A in-memory generic repository

    This class implements an in-memory solutoin for the generic repository interface.

    Note: This class is a unit test mock.
    """

    @abstractmethod
    def ident_from_model(self, entity: MODEL_T) -> IDENTITY_T:
        ...

    @abstractmethod
    def get_query_builder(self) -> IQueryBuilder:
        ...

    @override
    def save(self, entity: MODEL_T) -> MODEL_T:
        ident = self.ident_from_model(entity)
        if ident in self.storage:
            raise DuplicateEntityError(ident)
        self.storage[ident] = entity
        return entity

    @override
    def update(self, entity: MODEL_T) -> MODEL_T:
        ident = self.ident_from_model(entity)
        if ident not in self.storage:
            raise EntityNotFoundError(ident)
        self.storage[ident] = entity
        return entity

    @override
    def delete(self, ident: IDENTITY_T) -> None:
        try:
            del self.storage[ident]
        except KeyError:
            raise EntityNotFoundError(ident)

    @override
    def find_by_id(self, ident: IDENTITY_T) -> MODEL_T:
        if ident not in self.storage:
            raise EntityNotFoundError(ident)
        return self.storage[ident]

    @override
    def find_all(self) -> list[MODEL_T]:
        return list(self.storage.values())

    @override
    def find(self, filter: FilterPredicate) -> list[MODEL_T]:
        visitor = InMemoryRepoFilterVisitor()
        builder = self.get_query_builder()
        filter(builder).accept(visitor)
        return visitor.execute(self.storage.values())

    def __init__(self) -> None:
        self.storage: dict[IDENTITY_T, MODEL_T] = {}
