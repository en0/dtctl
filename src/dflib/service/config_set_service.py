import re

from re import compile as compile_re
from typing import final
#from uuid import UUID
#from pathlib import Path
from dflib.error import (
    DuplicateConfigSetError,
    DuplicateEntityError,
    InvalidConfigSetNameError,
)
from dflib.model import ConfigSet, ConfigSetEntry
from dflib.typing import (
    IConfigSetFileHandler,
    IRepository,
)


# Allow only a-z, A-Z, 0-9, ., -, and _
CONFIG_SET_NAME_PATTERN = compile_re(r"^[a-zA-Z0-9._-]+$")


@final
class ConfigSetService:
    """
    Service for managing configuration sets.

    This service provides the core business logic for managing configuration sets, including
    creating, deleting, adding files, removing files, listing all sets, retrieving specific sets,
    and retrieving file contents as bytes. The service handles file metadata and its raw content.
    """

    def create(self, config_set_name: str) -> ConfigSet:
        """
        Create a new configuration set.

        This method creates a new configuration set with the specified name. The configuration set
        is initially empty, with no associated files.

        Args:
            config_set_name (str): The name of the new configuration set.

        Returns:
            ConfigSet: The newly created configuration set.

        Raises:
            DuplicateConfigSetError: Raised if a configuration set with the same name already exists.
            OperationFailedError: Raised if the operation to create the configuration set fails.
            InvalidConfigSetNameError: Raised if the configuration set name is invalid.
        """

        config_set_name = str(config_set_name).strip()

        if len(config_set_name) > 25:
            raise InvalidConfigSetNameError(config_set_name)

        elif not config_set_name:
            raise InvalidConfigSetNameError(config_set_name)

        elif not CONFIG_SET_NAME_PATTERN.match(config_set_name):
            raise InvalidConfigSetNameError(config_set_name)

        cs = ConfigSet(config_set_name, [])

        try:
            return self._repo.save(cs)
        except DuplicateEntityError:
            raise DuplicateConfigSetError(config_set_name)

    def delete(self, config_set_name: str) -> None:
        """
        Delete an existing configuration set.

        This method deletes the configuration set with the specified name, including all associated
        files in the set.

        Args:
            config_set_name (str): The name of the configuration set to delete.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
            OperationFailedError: Raised if the operation to delete the configuration set fails.
        """
        raise NotImplementedError()

    def add_files(self, config_set_name: str, files: dict[str, bytes]) -> ConfigSet:
        """
        Add files to an existing configuration set.

        This method adds the specified files to the configuration set with the given name. Each file
        is represented as a key-value pair where the key is the file name and the value is the raw
        bytes of the file content.

        Args:
            config_set_name (str): The name of the configuration set to modify.
            files (dict[str, bytes]): A dictionary where keys are file names and values are file content as bytes.

        Returns:
            ConfigSet: The updated configuration set after the files are added.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
            FileAlreadyExistsError: Raised if one or more files already exist in the configuration set.
            OperationFailedError: Raised if the operation to add files fails.
        """
        raise NotImplementedError()

    def remove_files(self, config_set_name: str, files: list[str]) -> None:
        """
        Remove files from an existing configuration set.

        This method removes the specified files from the configuration set with the given name.
        Only file names are required for this operation.

        Args:
            config_set_name (str): The name of the configuration set to modify.
            files (list[str]): A list of file names to remove from the configuration set.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
            FileNotFoundError: Raised if one or more files are not part of the configuration set.
            OperationFailedError: Raised if the operation to remove files fails.
        """
        raise NotImplementedError()

    def all(self) -> list[ConfigSet]:
        """
        List all existing configuration sets.

        This method retrieves all configuration sets, including their names and associated files.

        Returns:
            list[ConfigSet]: A list of all configuration sets.

        Raises:
            QueryExecutionError: Raised if the operation to retrieve the configuration sets fails.
        """
        raise NotImplementedError()

    def get(self, config_set_name: str) -> ConfigSet:
        """
        Retrieve a specific configuration set by name.

        This method retrieves the configuration set with the specified name, including its associated files.

        Args:
            config_set_name (str): The name of the configuration set to retrieve.

        Returns:
            ConfigSet: The configuration set with the specified name.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
        """
        raise NotImplementedError()

    def get_file_bytes(self, config_set_name: str, file_name: str) -> bytes:
        """
        Retrieve the raw bytes of a specific file in a configuration set.

        This method retrieves the file content as bytes for the specified file in the given configuration set.

        Args:
            config_set_name (str): The name of the configuration set containing the file.
            file_name (str): The name of the file to retrieve.

        Returns:
            bytes: The raw bytes of the specified file.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
            FileNotFoundError: Raised if the specified file does not exist in the configuration set.
        """
        raise NotImplementedError()

    def __init__(
        self,
        config_set_repo: IRepository[ConfigSet, str],
        config_set_file_handler: IConfigSetFileHandler,
    ):
        """
        Initialize the ConfigSetService.

        Args:
            config_set_repo (IRepository[ConfigSet, str]): Repository for managing ConfigSet entities.
            config_set_file_handler (IConfigSetFileHandler): Handler for file management operations.
        """
        self._repo = config_set_repo
        self._file_handler = config_set_file_handler
