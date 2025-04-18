from typing import Any, final, override

from dflib.model import ConfigSet
from dflib.typing import IQueryBuilder, IFilterVisitor

from .repository_mock import RepositoryMock


@final
class ConfigSetRepositoryMock(RepositoryMock[ConfigSet, str]):
    """In-Memory Repository for ConfigSets.

    This class implements an in-memory repository mock for ConfigSets by extending the
    RepositoryMock.

    Note: This class is a unit test mock.
    """

    class _Builder(IQueryBuilder):

        @override
        def equals(self, field: str, value: Any) -> "ConfigSetRepositoryMock._Builder":
            self.eqs.append((field, value))
            return self

        @override
        def accept(self, visitor: IFilterVisitor) -> None:
            for f, v in self.eqs:
                visitor.visitEquals(f, v)

        @override
        def __init__(self):
            self.eqs: list[tuple[str, Any]] = []

    @override
    def ident_from_model(self, entity: ConfigSet) -> str:
        return entity.name

    @override
    def get_query_builder(self) -> IQueryBuilder:
        return self._Builder()

