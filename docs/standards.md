# Coding Standards for dflib Project

## Class and Method Documentation

- Every class and method should have a docstring that describes its purpose, responsibilities, and any important details.
- Use `Args` and `Attributes` sections in docstrings to document parameters and class attributes.

## Consistent Naming Conventions

- Use descriptive and consistent naming conventions for classes, methods, and variables.
- Class names should be in `PascalCase`, and method/variable names should be in `snake_case`.

## Exception Handling

- Custom exceptions should inherit from a base exception class (`DFError`).
- Each exception class must have a clear docstring explaining its purpose and attributes.
- Use descriptive error messages and include relevant attributes in exceptions.
- Methods should raise specific exceptions for error conditions, such as `EntityNotFoundError` or `DuplicateEntityError`.
- Docstrings should include what exceptions can be raised by a method.

## Interface and Abstract Classes

- Define interfaces and abstract classes using the `ABC` module.
- Use the `@abstractmethod` decorator for methods that must be implemented by subclasses.
- All interfaces should start with a capital i, 'I', followed by the rest of the name.
- Base classes should end with the name "Base".

```python
from abc import ABC, abstractmethod

class IMyInterface(ABC):
    @abstractmethod
    def add_number(self, a: list[int]) -> int:
        ...
```

## Type Hints

- Use type annotations for function arguments and return types to improve code readability and maintainability.
- Use `Any` for generic types when the specific type is not known.
- Use the `@override` decorator to indicate that a method is intended to override a method in a base class.
- Use the `@final` decorator to indicate that a class should not be subclassed.

### Examples

1. **Type Annotations for Function Arguments and Return Types**:

```python
class IRepository(Generic[MODEL_T, IDENTITY_T]):

    @abstractmethod
    def save(self, entity: MODEL_T) -> MODEL_T:
        raise NotImplementedError()
```

2. **Using `@final` Decorator**:

```python
from typing import final

@final
class ConfigSetService:
    ...
```

3. **Using `@override` Decorator**:

```python
from typing import override

class MyRepository(IRepository):

    @override
    def save(self, entity: MODEL_T) -> MODEL_T:
        ...
```

## Unit Tests

- Use mock classes to simulate dependencies in unit tests.
- Mock classes should end with the word "Mock" and be exposed in the `__all__` list of the module.
- Use fixtures for dependency injection.
- The `unit` fixture should always be included in each test file and represent the unit under test.
- Include tests that verify exception handling.
- Unit tests should follow the "given, when, then" structure.
- Unit tests do not require docstrings.

1. **The Unit Under Test**

```python
@pytest.fixture
def unit(
    mock_config_set_repo: IRepository[ConfigSet, str],
    config_set_file_handler: IConfigSetFileHandler,
) -> ConfigSetService:
    """
    Fixture for the ConfigSetService, initialized with mocked dependencies.
    """
    return ConfigSetService(mock_config_set_repo, config_set_file_handler)
```

2. **Testing for Exceptions**:

```python
def test_cannot_create_duplicate_config_set(
    unit: ConfigSetService,
    mock_config_set_repo: ConfigSetRepositoryMock
):
    # given
    name = DEFAULT_CONFIG_SET_NAME
    config_set = ConfigSet(name=name, files=[])
    _ = mock_config_set_repo.save(config_set)

    # when / then
    with pytest.raises(DuplicateConfigSetError):
        _ = unit.create(name)
```

3. **Mocking Dependencies**:
```python
def test_can_create_config_set(
    unit: ConfigSetService,
    mock_config_set_repo: ConfigSetRepositoryMock
):
    # given
    name = DEFAULT_CONFIG_SET_NAME

    # when
    _ = unit.create(name)

    # then
    assert [m.name for m in mock_config_set_repo.find_all()] == [name]
```
