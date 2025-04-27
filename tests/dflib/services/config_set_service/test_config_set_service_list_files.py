from pathlib import Path
from uuid import uuid4

import pytest

from dflib.error import ConfigSetNotFoundError
from dflib.model import ConfigSetEntry
from dflib.service import ConfigSetService
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *

from .fixtures import *


def test_list_files_in_existing_config_set(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: a configuration set with files exists in the repository
    file_names = ["file1.txt", "file2.txt", "file3.txt"]
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME, [ConfigSetEntry(uuid4(), Path(f)) for f in file_names]
    )
    _ = repo.save(config_set)

    # when: listing files in the configuration set
    result = unit.list_files(DEFAULT_CONFIG_SET_NAME)

    # then: the correct list of file names is returned
    assert set(result) == set(file_names)


def test_list_files_in_non_existent_config_set(unit: ConfigSetService):
    # given: a non-existent configuration set name
    non_existent_name = "non_existent_config_set"

    # when & then: attempting to list files in the non-existent configuration set
    with pytest.raises(ConfigSetNotFoundError):
        unit.list_files(non_existent_name)


def test_list_files_in_empty_config_set(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: an empty configuration set exists in the repository
    empty_config_set = ConfigSet(DEFAULT_CONFIG_SET_NAME, [])
    _ = repo.save(empty_config_set)

    # when: listing files in the configuration set
    result = unit.list_files(DEFAULT_CONFIG_SET_NAME)

    # then: an empty list is returned
    assert result == []


def test_list_files_with_special_characters(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: a configuration set with files having special characters in their names
    special_file_names = ["file@1.txt", "file#2.txt", "file&3.txt"]
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME, [ConfigSetEntry(uuid4(), Path(f)) for f in special_file_names]
    )
    _ = repo.save(config_set)


def test_list_files_with_large_number_of_files(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock
):
    # given: a configuration set with a large number of files
    large_file_names = [f"file_{i}.txt" for i in range(1000)]
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME, [ConfigSetEntry(uuid4(), Path(f)) for f in large_file_names]
    )
    _ = repo.save(config_set)

    # when: listing files in the configuration set
    result = unit.list_files(DEFAULT_CONFIG_SET_NAME)

    # then: the correct list of file names is returned
    assert set(result) == set(large_file_names)


def test_list_files_with_case_sensitivity(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: a configuration set with files having names that differ only in case
    case_sensitive_file_names = ["File.txt", "file.txt", "FILE.txt"]
    config_set = ConfigSet(
        DEFAULT_CONFIG_SET_NAME,
        [ConfigSetEntry(uuid4(), Path(f)) for f in case_sensitive_file_names],
    )
    _ = repo.save(config_set)

    # when: listing files in the configuration set
    result = unit.list_files(DEFAULT_CONFIG_SET_NAME)

    # then: the correct list of file names is returned
    assert set(result) == set(case_sensitive_file_names)
