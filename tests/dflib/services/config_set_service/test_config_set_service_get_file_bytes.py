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


def test_get_file_bytes(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: an existing config set with 1 file.
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME, [ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path(DEFAULT_FILE_PATH))]
    )
    config_set = repo.save(config_set)
    file_handler.store(DEFAULT_FILE_IDENTITY, DEFAULT_CONFIG_FILE_BYTES)

    # when: retrieve file bytes
    result = unit.get_file_bytes(DEFAULT_CONFIG_SET_NAME, DEFAULT_FILE_PATH)

    # then : file bytes should equal expected
    assert result == DEFAULT_CONFIG_FILE_BYTES


def test_config_set_not_found(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: No configset in repo
    # when: Retrieve file
    # then: ConfigSetNotFound
    with pytest.raises(ConfigSetNotFoundError):
        _ = unit.get_file_bytes(DEFAULT_CONFIG_SET_NAME, DEFAULT_FILE_PATH)


def test_file_not_found(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: A configset with no files
    config_set = ConfigSet(DEFAULT_CONFIG_SET_NAME, [])
    config_set = repo.save(config_set)

    # when: retrieve a file
    # then: ConfigsetNotFound
    with pytest.raises(FileReadError):
        result = unit.get_file_bytes(DEFAULT_CONFIG_SET_NAME, DEFAULT_FILE_PATH)
        print(result)


def test_empty_file(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: A configset with 1 file containing no data.
    file_handler.store(DEFAULT_FILE_IDENTITY, b"")
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME, [ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path(DEFAULT_FILE_PATH))]
    )
    config_set = repo.save(config_set)

    # when: Get the file contents
    result = unit.get_file_bytes(DEFAULT_CONFIG_SET_NAME, DEFAULT_FILE_PATH)

    # then: File contents should be empty
    assert result == b""


def test_large_file(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given: A configset with 1 file containing a lot of data
    file_contents = b"".join([int.to_bytes(i, 1) for i in range(0, 255)]) * 100
    file_handler.store(DEFAULT_FILE_IDENTITY, file_contents)
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME, [ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path(DEFAULT_FILE_PATH))]
    )
    config_set = repo.save(config_set)

    # when: the file is retrieved...
    result = unit.get_file_bytes(DEFAULT_CONFIG_SET_NAME, DEFAULT_FILE_PATH)

    # then: the file contents are complete and correct
    assert result == file_contents


def test_file_name_with_special_chars(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock
):
    # given
    file_contents = "✗".encode("utf-8")
    file_handler.store(DEFAULT_FILE_IDENTITY, file_contents)
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME, [ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path(DEFAULT_FILE_PATH))]
    )
    config_set = repo.save(config_set)

    # when: the file is retrieved...
    result = unit.get_file_bytes(DEFAULT_CONFIG_SET_NAME, DEFAULT_FILE_PATH)

    # then: the file contents are complete and correct
    assert result == file_contents
