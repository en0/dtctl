import pytest

from dflib.service import ConfigSetService
from dflib.error import ConfigSetNotFoundError, FileNotFoundError

from tests.fixtures import *
from tests.mocks import *
from tests.helpers import *

from .fixtures import *


def test_files_are_removed_from_configuration_set(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
):
    # given: a configuration set with multiple files
    config_set_name = DEFAULT_CONFIG_SET_NAME

    _ = unit.create(config_set_name)

    files_to_add: dict[str, bytes] = {
        DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES,
        DEFAULT_CONFIG_FILE_NAME+'2': DEFAULT_CONFIG_FILE_BYTES + b'2',
    }
    _ = unit.add_files(config_set_name, files_to_add)

    # when: Remove a specific file from the configuration set
    _ = unit.remove_files(config_set_name, [DEFAULT_CONFIG_FILE_NAME])

    # then: Verify that the specified file has been removed
    config_set = repo.find_by_id(config_set_name)
    print(config_set)
    assert len(config_set.files) == 1
    assert all(str(file.name) == DEFAULT_CONFIG_FILE_NAME+'2' for file in config_set.files)


def test_remove_nonexistent_file_raises_error(unit: ConfigSetService):
    # given: a configuration set with a single file
    config_set_name = DEFAULT_CONFIG_SET_NAME
    files_to_add = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}
    _ = unit.create(config_set_name)
    _ = unit.add_files(config_set_name, files_to_add)

    # when / then: Attempt to remove a nonexistent file and expect a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        _ = unit.remove_files(config_set_name, ["nonexistent_file.txt"])


def test_remove_from_nonexistent_config_set_raises_error(unit: ConfigSetService):
    # given: a nonexistent configuration set
    config_set_name = "nonexistent_config_set"

    # when / then: Attempt to remove a file from a nonexistent configuration set and expect a ConfigSetNotFoundError
    with pytest.raises(ConfigSetNotFoundError):
        _ = unit.remove_files(config_set_name, ["file1.txt"])


def test_remove_files_returns_none(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
    file_handler: ConfigSetFileHandlerMock
):
    # given: a configuration set with multiple files
    config_set_name = "test_config_set"
    _ = unit.create(config_set_name)
    files_to_add = {"file1.txt": b"content1", "file2.txt": b"content2"}
    _ = unit.add_files(config_set_name, files_to_add)

    # when: Remove a file from the configuration set
    updated_config_set = unit.remove_files(config_set_name, ["file1.txt"])

    # then: Verify that the method returns the updated configuration set with the remaining files
    assert len(updated_config_set.files) == 1
    assert all(str(file.name) == "file2.txt" for file in updated_config_set.files)


def test_remove_specified_files_from_config_set(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
):
    # given: a configuration set with multiple files
    config_set_name = DEFAULT_CONFIG_SET_NAME

    _ = unit.create(config_set_name)
    files_to_add: dict[str, bytes] = {
        DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES,
        DEFAULT_CONFIG_FILE_NAME + '2': DEFAULT_CONFIG_FILE_BYTES + b'2',
    }
    _ = unit.add_files(config_set_name, files_to_add)

    # when: Remove a specific file from the configuration set
    _ = unit.remove_files(config_set_name, [DEFAULT_CONFIG_FILE_NAME])

    # then: Verify that the specified file has been removed
    config_set = repo.find_by_id(config_set_name)
    assert len(config_set.files) == 1
    assert all(str(file.name) == DEFAULT_CONFIG_FILE_NAME + '2' for file in config_set.files)


def test_remove_multiple_files_successfully(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
):
    # given: a configuration set with multiple files
    config_set_name = DEFAULT_CONFIG_SET_NAME

    _ = unit.create(config_set_name)
    files_to_add: dict[str, bytes] = {
        DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES,
        DEFAULT_CONFIG_FILE_NAME + '2': DEFAULT_CONFIG_FILE_BYTES + b'2',
        DEFAULT_CONFIG_FILE_NAME + '3': DEFAULT_CONFIG_FILE_BYTES + b'3',
    }
    _ = unit.add_files(config_set_name, files_to_add)

    # when: Remove multiple files from the configuration set
    _ = unit.remove_files(config_set_name, [DEFAULT_CONFIG_FILE_NAME, DEFAULT_CONFIG_FILE_NAME + '2'])

    # then: Verify that the specified files have been removed
    config_set = repo.find_by_id(config_set_name)
    assert len(config_set.files) == 1
    assert all(str(file.name) == DEFAULT_CONFIG_FILE_NAME + '3' for file in config_set.files)


def test_update_config_set_after_removal(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
):
    # given: a configuration set with multiple files
    config_set_name = DEFAULT_CONFIG_SET_NAME

    _ = unit.create(config_set_name)
    files_to_add: dict[str, bytes] = {
        DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES,
        DEFAULT_CONFIG_FILE_NAME + '2': DEFAULT_CONFIG_FILE_BYTES + b'2',
    }
    _ = unit.add_files(config_set_name, files_to_add)

    # when: Remove a file from the configuration set
    _ = unit.remove_files(config_set_name, [DEFAULT_CONFIG_FILE_NAME])

    # then: Verify that the configuration set is updated correctly
    config_set = repo.find_by_id(config_set_name)
    assert len(config_set.files) == 1
    assert all(str(file.name) == DEFAULT_CONFIG_FILE_NAME + '2' for file in config_set.files)


def test_raise_config_set_not_found_error(unit: ConfigSetService):
    # given: a nonexistent configuration set
    non_existent_config_set_name = "non_existent_config_set"
    files_to_remove = ["file1.txt"]

    # when / then: Attempt to remove a file from a nonexistent configuration set and expect a ConfigSetNotFoundError
    with pytest.raises(ConfigSetNotFoundError):
        _ = unit.remove_files(non_existent_config_set_name, files_to_remove)


def test_raise_file_not_found_error(unit: ConfigSetService):
    # given: a configuration set with a single file
    config_set_name = DEFAULT_CONFIG_SET_NAME
    files_to_add = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}
    _ = unit.create(config_set_name)
    _ = unit.add_files(config_set_name, files_to_add)

    # when / then: Attempt to remove a nonexistent file and expect a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        _ = unit.remove_files(config_set_name, ["nonexistent_file.txt"])


def test_remove_files_with_empty_list(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: a configuration set with some files
    config_set_name = DEFAULT_CONFIG_SET_NAME
    files_to_add = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}
    _ = unit.create(config_set_name)
    _ = unit.add_files(config_set_name, files_to_add)

    # when: an empty list is passed to remove_files
    updated_config_set = unit.remove_files(config_set_name, [])

    # then: ensure no operation occurs and the files remain unchanged
    assert len(updated_config_set.files) == 1
    assert all(str(file.name) == DEFAULT_CONFIG_FILE_NAME for file in updated_config_set.files)


def test_remove_files_with_duplicate_names(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: a configuration set with some files
    config_set_name = DEFAULT_CONFIG_SET_NAME
    files_to_add = {
        DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES,
        DEFAULT_CONFIG_FILE_NAME + '2': DEFAULT_CONFIG_FILE_BYTES + b'2',
    }
    _ = unit.create(config_set_name)
    _ = unit.add_files(config_set_name, files_to_add)

    # when: duplicate file names are passed to remove_files
    _ = unit.remove_files(config_set_name, [DEFAULT_CONFIG_FILE_NAME, DEFAULT_CONFIG_FILE_NAME])

    # then: ensure duplicates are ignored, but the files are still removed
    config_set = repo.find_by_id(config_set_name)
    assert len(config_set.files) == 1
    assert all(str(file.name) == DEFAULT_CONFIG_FILE_NAME + '2' for file in config_set.files)


def test_remove_files_case_sensitivity(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: a configuration set with files having names differing only by case
    config_set_name = DEFAULT_CONFIG_SET_NAME
    files_to_add = {
        "file.txt": b"content1",
        "File.txt": b"content2",
    }
    _ = unit.create(config_set_name)
    _ = unit.add_files(config_set_name, files_to_add)

    # when: a file name with a specific case is passed to remove_files
    _ = unit.remove_files(config_set_name, ["file.txt"])

    # then: ensure only the file with the exact case is removed
    config_set = repo.find_by_id(config_set_name)
    assert len(config_set.files) == 1
    assert all(str(file.name) == "File.txt" for file in config_set.files)


## TODO: Implement this test when we make a decision on the underlying storage mech.
def test_remove_files_partial_success(unit: ConfigSetService):
    # given: a configuration set with some files
    # when: some files are successfully removed and others are not
    # then: define behavior for partial success
    assert True
