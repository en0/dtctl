from abc import ABC, abstractmethod
from uuid import UUID


class IConfigSetFileHandler(ABC):
    """
    Interface for managing configuration files in the dotfiles repository.

    This interface defines methods for storing, retrieving, and removing configuration files in the
    dotfiles repository. Each configuration file is uniquely identified by a UUID (`ident`), and its
    content is represented as raw bytes (`data`).

    The `store` method allows writing data into the repository, with an optional flag to overwrite
    existing files. The `retrieve` method retrieves the file data associated with a specific
    identifier, and the `remove` method deletes the file from the repository.

    Responsibilities:
        - Abstract file storage and retrieval operations.
        - Handle errors related to file operations, such as read/write failures or conflicts.
        - Provide a clean and consistent interface for managing configuration files.

    Methods:
        - `store(ident: UUID, data: bytes, overwrite: bool = False) -> None`: Write data to the repository.
        - `retrieve(ident: UUID) -> bytes`: Retrieve data from the repository.
        - `remove(ident: UUID) -> None`: Remove data from the repository.

    Exception Handling:
        - `FileWriteError`: Raised when a write operation fails.
        - `FileConflictError`: Raised when writing to an existing file without `overwrite`.
        - `FileReadError`: Raised when a read operation fails.
        - `FileNotFoundError`: Raised when attempting to retrieve or remove a nonexistent file.

    This interface is designed to be extended and implemented in various storage backends,
    such as file systems, databases, and/or remote APIs.
    """

    @abstractmethod
    def store(self, ident: UUID, data: bytes, overwrite: bool = False) -> None:
        """
        Write a configuration file into the dotfiles repository.

        This method stores the given `data` into the dotfiles repository under the given `ident`.
        If the `overwrite` flag is set, the operation will replace any existing data stored under
        the given `ident` if any exists.

        Args:
            ident (UUID): The identity of the configuration file.
            data (bytes): The bytes that makeup the file to be stored.
            overwrite (bool): A flag indicating if the operation is allowed to replace an existing
                              file. Default: False

        Raises:
            FileWriteError: Raised if the destination could not be written for any reason.
            FileConflictError Raised if the destination file exists.
        """
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, ident: UUID) -> bytes:
        """
        Retrieves a configuration file from the dotfiles repository.

        This method retrieves the bytes for the configuration in the dotfiles repository associated
        with the given `ident`.

        Args:
            ident (UUID): The identity of the configuration file.

        Raises:
            FileReadError: Raised if the file to store could not be read for any reason.

        Returns:
            The `bytes` of the configuration file.
        """
        raise NotImplementedError()

    @abstractmethod
    def remove(self, ident: UUID) -> None:
        """
        Remove a file from the dotfiles repository.

        This method removes the configuration file from the dotfile repository associated with the
        given `ident`.

        Args:
            ident (UUID): The identity of the configuration file.

        Raises:
            FileReadError: Raised if the file to store could not be read for any reason.
        """
        raise NotImplementedError()
