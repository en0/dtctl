from pathlib import Path
from re import compile as compile_re
from typing import final
from uuid import uuid4

from dflib.error import (
    ConfigFileAlreadyExistsError,
    ConfigFileNameInvalidError,
    ConfigSetNotFoundError,
    DuplicateConfigSetError,
    DuplicateEntityError,
    EntityNotFoundError,
    FileReadError,
    FileWriteError,
    InvalidConfigSetNameError,
    OperationFailedError,
    QueryExecutionError,
)
from dflib.model import ConfigSet, ConfigSetEntry
from dflib.typing import IConfigSetFileHandler, IRepository

# Allow only a-z, A-Z, 0-9, ., -, and _
CONFIG_SET_NAME_PATTERN = compile_re(r"^[a-zA-Z0-9._-]+$")
INVALID_FILENAME_PATTERN = compile_re(r'[<>:"|?*{}!$%]')


@final
class ConfigSetService:
    """
    Service for managing configuration sets.

    This service provides the core business logic for managing configuration sets, including
    creating, deleting, adding files, removing files, listing all sets, retrieving specific sets,
    and retrieving file contents as bytes. The service handles file metadata and its raw content.
    """

    def create(self, config_set_name: str) -> None:
        """
        Create a new configuration set.

        This method creates a new configuration set with the specified name. The configuration set
        is initially empty, with no associated files.

        Args:
            config_set_name (str): The name of the new configuration set.

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
            _ = self._repo.save(cs)
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
        """
        try:
            config_set = self._repo.find_by_id(config_set_name)
            for file in config_set.files:
                try:
                    self._file_handler.remove(file.id)
                except FileReadError:
                    pass
            self._repo.delete(config_set_name)
        except EntityNotFoundError:
            raise ConfigSetNotFoundError(config_set_name)

    def add_files(self, config_set_name: str, files: dict[str, bytes]) -> list[str]:
        """
        Add files to an existing configuration set.

        This method adds the specified files to the configuration set with the given name. Each file
        is represented as a key-value pair where the key is the file name and the value is the raw
        bytes of the file content.

        Args:
            config_set_name (str): The name of the configuration set to modify.
            files (dict[str, bytes]): A dictionary where keys are file names and values are file
                content as bytes.

        Returns:
            list[str]: A list of file names that were added to the configuration set.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
            ConfigFileAlreadyExistsError: Raised if one or more files already exist in the
                configuration set.
            OperationFailedError: Raised if the operation to add files fails.
        """

        try:

            config_set = self._repo.find_by_id(config_set_name)
            existing_files = {entry.name for entry in config_set.files}

            for file_name, file_bytes in files.items():
                if (
                    file_name == ""
                    or file_name == "."
                    or file_name.endswith("\\")
                    or file_name.endswith("/")
                ):
                    raise ConfigFileNameInvalidError(file_name)

                elif INVALID_FILENAME_PATTERN.search(file_name):
                    raise ConfigFileNameInvalidError(file_name)

                elif Path(file_name) in existing_files:
                    raise ConfigFileAlreadyExistsError(config_set_name, file_name)

                entry = ConfigSetEntry(id=uuid4(), name=Path(file_name))
                config_set.files.append(entry)
                self._file_handler.store(entry.id, file_bytes)

            _ = self._repo.update(config_set)
            return [str(entry.name) for entry in config_set.files]

        except EntityNotFoundError:
            raise ConfigSetNotFoundError(config_set_name)

        except FileWriteError as e:
            raise OperationFailedError("add_files", str(e))

    def remove_files(self, config_set_name: str, files: list[str]) -> list[str]:
        """
        Remove files from an existing configuration set.

        This method removes the specified files from the configuration set with the given name.
        Only file names are required for this operation.

        Args:
            config_set_name (str): The name of the configuration set to modify.
            files (list[str]): A list of file names to remove from the configuration set.

        Returns:
            list[str]: A list of remaining file names in the configuration set after removal.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
            FileNotFoundError: Raised if one or more files are not part of the configuration set.
            OperationFailedError: Raised if the operation to remove files fails.
        """

        try:
            config_set = self._repo.find_by_id(config_set_name)

            file_keys = {Path(f) for f in files}
            existing_files = {entry.name for entry in config_set.files}
            missing_files = file_keys - existing_files

            for f in missing_files:
                raise FileReadError(str(f))

            for entry_to_remove in [entry for entry in config_set.files if entry.name in file_keys]:
                config_set.files.remove(entry_to_remove)
                self._file_handler.remove(entry_to_remove.id)

            _ = self._repo.update(config_set)
            return [str(f.name) for f in config_set.files]

        except EntityNotFoundError:
            raise ConfigSetNotFoundError(config_set_name)

    def list_config_sets(self) -> list[str]:
        """
        List all existing configuration sets.

        This method retrieves all configuration sets, including their names and associated files.

        Returns:
            list[str]: A list of all configuration set names.

        Raises:
            OperationFailedError: Raised if the operation to delete the configuration set fails.
        """
        try:
            # Retrieve all configuration sets from the repository
            config_sets = self._repo.find_all()

            # Return a list of configuration set names
            return [config_set.name for config_set in config_sets]
        except QueryExecutionError as ex:
            raise OperationFailedError("list_config_sets", str(ex))

    def list_files(self, config_set_name: str) -> list[str]:
        """
        Retrieve a specific configuration set by name.

        This method retrieves the configuration set with the specified name, including its associated files.

        Args:
            config_set_name (str): The name of the configuration set to retrieve.

        Returns:
            list[str]: A list of file names in the specified configuration set.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
        """
        try:
            config_set = self._repo.find_by_id(config_set_name)
            return [str(entry.name) for entry in config_set.files]
        except EntityNotFoundError:
            raise ConfigSetNotFoundError(config_set_name)

    def get_file_bytes(self, config_set_name: str, file_name: str) -> bytes:
        """
        Retrieve the raw bytes of a specific file in a configuration set.

        This method retrieves the file content as bytes for the specified file in the given configuration set.

        Args:
            config_set_name (str): The name of the configuration set containing the file.
            file_name (str): The name of the file to retrieve.

        Returns:
            bytes: The content of the specified file as bytes.

        Raises:
            ConfigSetNotFoundError: Raised if the configuration set does not exist.
            FileNotFoundError: Raised if the specified file does not exist in the configuration set.
        """
        try:
            config_set = self._repo.find_by_id(config_set_name)
            file = [f for f in config_set.files if str(f.name) == file_name][0]
            return self._file_handler.retrieve(file.id)

        except IndexError:
            raise FileReadError(file_name)

        except EntityNotFoundError:
            raise ConfigSetNotFoundError(config_set_name)

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
