import pytest

from dflib.service import ConfigSetService
from dflib.typing import IRepository, IConfigSetFileHandler
from dflib.model import ConfigSet
from dflib.error import FileNotFoundError

from tests.fixtures import *
from tests.mocks import *
from tests.helpers import *

from .fixtures import *


# TODO: implement these test
"""
- Test that the method removes the specified files from the configuration set.
- Test that the method raises an exception if the configuration set does not exist.
- Test that the method raises an exception if any of the specified files do not exist in the configuration set.
- Test that the method returns None after successful removal.
"""

def test_files_are_removed_from_configuration_set(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
):
    # given
    config_set_name = DEFAULT_CONFIG_SET_NAME

    _ = unit.create(config_set_name)

    files_to_add: dict[str, bytes] = {
        DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES,
        DEFAULT_CONFIG_FILE_NAME+'2': DEFAULT_CONFIG_FILE_BYTES + b'2',
    }
    _ = unit.add_files(config_set_name, files_to_add)

    # when
    unit.remove_files(config_set_name, [DEFAULT_CONFIG_FILE_NAME])

    # then
    config_set = repo.find_by_id(config_set_name)
    print(config_set)
    assert len(config_set.files) == 1
    assert all(str(file.name) == DEFAULT_CONFIG_FILE_NAME+'2' for file in config_set.files)


def test_remove_nonexistent_file_raises_error(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
    file_handler: ConfigSetFileHandlerMock
):
    # given
    config_set_name = DEFAULT_CONFIG_SET_NAME
    files_to_add = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}
    _ = unit.create(config_set_name)
    _ = unit.add_files(config_set_name, files_to_add)

    # when / then
    with pytest.raises(FileNotFoundError):
        unit.remove_files(config_set_name, ["nonexistent_file.txt"])


#def test_remove_from_nonexistent_config_set_raises_error(
#    unit: ConfigSetService,
#    repo: ConfigSetRepositoryMock,
#    file_handler: ConfigSetFileHandlerMock
#):
#    # given
#    config_set_name = "nonexistent_config_set"
#
#    # when / then
#    with pytest.raises(ConfigSetNotFoundError):
#        unit.remove_files(config_set_name, ["file1.txt"])
#
#
#def test_remove_files_returns_none(
#    unit: ConfigSetService,
#    repo: ConfigSetRepositoryMock,
#    file_handler: ConfigSetFileHandlerMock
#):
#    # given
#    config_set_name = "test_config_set"
#    files_to_add = {"file1.txt": b"content1", "file2.txt": b"content2"}
#    unit.add_files(config_set_name, files_to_add)
#
#    # when
#    result = unit.remove_files(config_set_name, ["file1.txt"])
#
#    # then
#    assert result is None
#
