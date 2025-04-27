from pathlib import Path
from uuid import uuid4

import pytest

from dflib.error import ConfigSetNotFoundError, FileReadError
from dflib.model import ConfigSetEntry
from dflib.service import ConfigSetService
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *

from .fixtures import *


def test_delete_config_set_with_no_files(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: a config set exists in the repository
    _ = repo.save(ConfigSet(DEFAULT_CONFIG_SET_NAME, []))

    # when: delete configset
    unit.delete(DEFAULT_CONFIG_SET_NAME)

    # then: the configset no longer exists in the repository.
    assert repo.find_all() == []


def test_deletes_config_set_with_many_files(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: a config set exists and has files
    files = [ConfigSetEntry(uuid4(), Path(f"file_{i}.txt")) for i in range(10)]
    config_set = ConfigSet(DEFAULT_CONFIG_SET_NAME, files)
    _ = repo.save(config_set)

    # when: delete configset
    unit.delete(DEFAULT_CONFIG_SET_NAME)

    # then: the configset no longer exists in the repository.
    assert repo.find_all() == []


def test_deletes_the_file_contents(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: a config set exists and has files
    files = [ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path("file.txt"))]
    config_set = ConfigSet(DEFAULT_CONFIG_SET_NAME, files)
    file_handler.store(DEFAULT_FILE_IDENTITY, b"Hello, world!")
    _ = repo.save(config_set)

    # when: delete configset
    unit.delete(DEFAULT_CONFIG_SET_NAME)

    # then: the file was deleted
    with pytest.raises(FileReadError):
        _ = file_handler.retrieve(DEFAULT_FILE_IDENTITY)


def test_raises_config_not_found(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: no config exists
    # when: delete configset
    # then: service raises config not found error
    with pytest.raises(ConfigSetNotFoundError):
        unit.delete(DEFAULT_CONFIG_SET_NAME)


def test_ignores_missing_files(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: a config set exists with files and file content doesn't exist
    files = [ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path("file.txt"))]
    config_set = ConfigSet(DEFAULT_CONFIG_SET_NAME, files)
    _ = repo.save(config_set)

    # when: delete configset
    unit.delete(DEFAULT_CONFIG_SET_NAME)

    # then: the file was deleted
    assert True
