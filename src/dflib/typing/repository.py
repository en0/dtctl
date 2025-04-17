from typing import Generic, TypeVar, Any, Callable
from abc import abstractmethod, ABC


MODEL_T = TypeVar("MODEL_T")
IDENTITY_T = TypeVar("IDENTITY_T")


FilterPredicate = Callable[["IQueryBuilder"], "IQueryBuilder | None"]


class IFilterVisitor(ABC):
    """
    Visitor interface for processing filters.

    This interface defines methods for various filter types, allowing the repository to translate
    abstract filters into optimized queries for specific underlying technologies.

    Responsibilities:
        - Abstract the logic for processing filters into a visitor pattern.
        - Support translation of domain-level filter criteria to technology-specific queries.
        - Provide methods for handling various filter operations, such as equality checks.

    Methods:
        - `visitEquals(field: str, value: str) -> None`: Process an equals filter condition.
    """

    @abstractmethod
    def visitEquals(self, field: str, value: str) -> None:
        """
        Visit an equals filter, which represents a condition where the field
        must equal a specific value.

        Args:
            field (str): The name of the field to filter on.
            value (str): The value that the field must equal.

        Raises:
            QueryExecutionError: if there is an error while processing the filter.
        """
        raise NotImplementedError()


class IQueryBuilder(ABC):
    """
    Interface for building filters.

    This interface provides methods to construct domain-level filters in a declarative way.
    Filters built using this interface can later be applied to repositories or other query systems.

    Responsibilities:
        - Facilitate the creation of filter conditions.
        - Support chaining of filter operations for complex queries.
        - Provide a mechanism to accept a filter visitor for query translation.

    Methods:
        - `equals(field: str, value: Any) -> IQueryBuilder`: Add an equality condition.
        - `accept(visitor: IFilterVisitor) -> None`: Accept a visitor for processing the filter.
    """

    @abstractmethod
    def equals(self, field: str, value: Any) -> "IQueryBuilder":
        """
        Add an equals condition to the filter.

        Args:
            field (str): The name of the field to filter on.
            value (Any): The value to compare the field against.

        Returns:
            IQueryBuilder: The current instance of the filter builder, allowing method chaining.

        Raises:
            QueryExecutionError: if there is an error while processing the filter.
        """
        raise NotImplementedError()

    @abstractmethod
    def accept(self, visitor: IFilterVisitor) -> None:
        """
        Accept a filter visitor for processing the filter.

        Args:
            visitor (IFilterVisitor): The visitor that will process the filter.

        Raises:
            QueryExecutionError: If there is an error while processing the filter visitor.
        """
        raise NotImplementedError()


class IRepository(Generic[MODEL_T, IDENTITY_T]):
    """
    Generic repository interface for CRUD operations and filtered queries.

    This interface abstracts data access logic, allowing the service layer to work with the repository
    without being coupled to the underlying storage technology. It provides common operations for
    saving, updating, deleting, and querying entities.

    Responsibilities:
        - Abstract CRUD operations for entities identified by unique keys.
        - Support domain-level filtering using predicates or filters.
        - Provide methods to retrieve single or multiple entities.

    Methods:
        - `save(entity: MODEL_T) -> MODEL_T`: Persist a new entity.
        - `update(entity: MODEL_T) -> MODEL_T`: Update an existing entity.
        - `delete(id: IDENTITY_T) -> None`: Delete an entity by its identifier.
        - `find_by_id(ident: IDENTITY_T) -> MODEL_T`: Retrieve an entity by its identifier.
        - `find_all() -> list[MODEL_T]`: Retrieve all entities.
        - `find(filter: Predicate) -> list[MODEL_T]`: Retrieve entities matching a given filter.
    """

    @abstractmethod
    def save(self, entity: MODEL_T) -> MODEL_T:
        """
        Persist a new entity to the repository.

        Args:
            entity (MODEL_T): The entity to be saved.

        Returns:
            MODEL_T: The saved entity.

        Raises:
            DuplicateEntityError: If an entity with the same identifier already exists.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: MODEL_T) -> MODEL_T:
        """
        Update an existing entity in the repository.

        Args:
            entity (MODEL_T): The entity to be updated.

        Returns:
            MODEL_T: The updated entity.

        Raises:
            EntityNotFoundError: If the entity to update does not exist.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: IDENTITY_T) -> None:
        """
        Delete an entity from the repository by its identifier.

        Args:
            id (IDENTITY_T): The unique identifier of the entity to delete.

        Raises:
            EntityNotFoundError: If the entity to delete does not exist.
        """
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, ident: IDENTITY_T) -> MODEL_T:
        """
        Retrieve an entity by its unique identifier.

        Args:
            ident (IDENTITY_T): The unique identifier of the entity.

        Returns:
            MODEL_T: The entity if found, or raises an exception if not found.

        Raises:
            EntityNotFoundError: If the entity is not found.
        """
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> list[MODEL_T]:
        """
        Retrieve all entities from the repository.

        Returns:
            list[MODEL_T]: A list of all entities.

        Raises:
            QueryExecutionError: If there is an error while fetching the entities.
        """
        raise NotImplementedError()

    @abstractmethod
    def find(self, filter: FilterPredicate) -> list[MODEL_T]:
        """
        Retrieve entities that match the given filter criteria.

        Args:
            filter (Predicate): A callable that defines the query criteria using a filter builder.

        Returns:
            list[MODEL_T]: The list of entities matching the filter criteria.

        Raises:
            QueryExecutionError: If there is an error while executing the filter.
        """
        raise NotImplementedError()

