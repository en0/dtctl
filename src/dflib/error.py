"""All exception classes for dflib"""

from typing import Any


class DFError(Exception):
    """Base class for all exceptions raised by dflib."""

    pass


class FileReadError(DFError):
    """
    Exception raised when there is an issue reading a file.

    This exception is intended to capture errors that occur while attempting to access or read a
    file.

    Attributes:
        file_path (str): The path of the file that could not be read.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "Unable to read file."):
        super().__init__(message)
        self.file_path: str = file_path


class FileNotFoundError(FileReadError):
    """
    Exception raised when a read operation is attempted against a non-existant file path.

    This exception is a specialized form of `FileReadError` and is intended to capture cases where a
    file read operation fails because the source file does not exist.

    Attributes:
        file_path (str): The path of the file that caused the conflict.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "File not found."):
        super().__init__(file_path, message)


class FileWriteError(DFError):
    """
    Exception raised when there is an issue writing a file.

    This exception is intended to capture errors that occur while attempting to write data to a
    file.

    Attributes:
        file_path (str): The path of the file that could not be written.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "Unable to write file."):
        super().__init__(message)
        self.file_path: str = file_path


class FileConflictError(FileWriteError):
    """
    Exception raised when there is a conflict while attempting to write a file.

    This exception is a specialized form of `FileWriteError` and is intended to capture cases where
    a file write operation fails due to a conflict. For example, this might occur if the file
    already exists and overwriting is not allowed.

    Attributes:
        file_path (str): The path of the file that caused the conflict.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "Unable to write file due to conflict."):
        super().__init__(message)
        self.file_path: str = file_path


class EntityNotFoundError(DFError):
    """
    Exception raised when an entity is not found in the repository.

    Attributes:
        identifier (Any): The identifier of the missing entity.
    """

    def __init__(self, identifier: Any):
        self.identifier: Any = identifier
        super().__init__(f"No entity with identifier '{identifier}' was not found.")


class DuplicateEntityError(DFError):
    """
    Exception raised when attempting to save a duplicate entity.

    Attributes:
        identifier (Any): The identifier of the conflicting entity.
    """

    def __init__(self, identifier: Any):
        self.identifier: Any = identifier
        super().__init__(f"Duplicate entity with identifier '{identifier}'.")


class QueryExecutionError(DFError):
    """
    Exception raised when a query fails to execute.

    Attributes:
        query (str): The query that failed.
        reason (str): A description of the failure reason.
    """

    def __init__(self, query: str, reason: str):
        self.query: str = query
        self.reason: str = reason
        super().__init__(f"Query failed: {reason}. Query: {query}")


class DuplicateConfigSetError(DFError):
    """
    Exception raised when attempting to create a configuration set with a name that already exists.

    Args:
        config_set_name (str): The name of the duplicate configuration set.

    Attributes:
        config_set_name (str): The name of the duplicate configuration set.
    """

    def __init__(self, config_set_name: str):
        self.config_set_name: str = config_set_name
        super().__init__(f"A configuration set with the name '{config_set_name}' already exists.")


class ConfigSetNotFoundError(DFError):
    """
    Exception raised when a configuration set is not found.

    Args:
        config_set_name (str): The name of the configuration set that was not found.

    Attributes:
        config_set_name (str): The name of the configuration set that was not found.
    """

    def __init__(self, config_set_name: str):
        self.config_set_name: str = config_set_name
        super().__init__(f"The configuration set '{config_set_name}' was not found.")


class ConfigFileAlreadyExistsError(DFError):
    """
    Exception raised when attempting to add a file that already exists in a configuration set.

    Args:
        config_set_name (str): The name of the configuration set.
        file_name (str): The name of the file that already exists.

    Attributes:
        config_set_name (str): The name of the configuration set.
        file_name (str): The name of the file that already exists.
    """

    def __init__(self, config_set_name: str, file_name: str):
        self.config_set_name: str = config_set_name
        self.file_name: str = file_name
        super().__init__(
            f"The file '{file_name}' already exists in the configuration set '{config_set_name}'."
        )


class ConfigFileNotFoundError(DFError):
    """
    Exception raised when a file is not found in a configuration set.

    Args:
        config_set_name (str): The name of the configuration set.
        file_name (str): The name of the file that was not found.

    Attributes:
        config_set_name (str): The name of the configuration set.
        file_name (str): The name of the file that was not found.
    """

    def __init__(self, config_set_name: str, file_name: str):
        self.config_set_name: str = config_set_name
        self.file_name: str = file_name
        super().__init__(
            f"The file '{file_name}' was not found in the configuration set '{config_set_name}'."
        )


class ConfigFileNameInvalidError(DFError):
    """
    Exception raised when an invalid file name is provided for a configuration set.

    Args:
        file_name (str): The invalid file name.

    Attributes:
        file_name (str): The invalid file name.
    """

    def __init__(self, file_name: str):
        self.file_name: str = file_name
        super().__init__(f"The file name '{file_name}' is invalid.")


class InvalidConfigSetNameError(DFError):
    """
    Exception raised when an invalid configuration set name is provided.

    Args:
        config_set_name (str): The invalid configuration set name.

    Attributes:
        config_set_name (str): The invalid configuration set name.
    """

    def __init__(self, config_set_name: str):
        self.config_set_name: str = config_set_name
        super().__init__(f"The configuration set name '{config_set_name}' is invalid.")


class OperationFailedError(DFError):
    """
    Exception raised when an operation on a configuration set fails.

    Args:
        operation (str): The name of the operation that failed.
        reason (str | None): Optional reason or message explaining the failure.

    Attributes:
        operation (str): The name of the operation that failed.
    """

    def __init__(self, operation: str, reason: str | None = None):
        self.operation: str = operation
        message = f"The operation '{operation}' failed."
        if reason:
            message += f" Reason: {reason}"
        super().__init__(message)
