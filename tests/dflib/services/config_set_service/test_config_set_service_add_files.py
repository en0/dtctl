import pytest

from pathlib import Path
from uuid import UUID
from dflib.service import ConfigSetService
from dflib.model import ConfigSet, ConfigSetEntry
from dflib.error import ConfigFileNameInvalidError, ConfigSetNotFoundError, ConfigFileAlreadyExistsError, FileWriteError, OperationFailedError

from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *

from .fixtures import *


# TODO: TEst Cases to implement
"""
- **Transaction Consistancy**: Failed operations should not leave partially completed work.
"""


def test_add_files_success(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given
    files = {
        DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES,
        DEFAULT_CONFIG_FILE_NAME + '2': DEFAULT_CONFIG_FILE_BYTES + b'2',
    }
    _ = repo.save(ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[]))

    # when
    updated_config_set = unit.add_files(DEFAULT_CONFIG_SET_NAME, files)

    # then
    assert len(updated_config_set.files) == 2
    print(updated_config_set)
    assert all(str(file.name) in files for file in updated_config_set.files)


def test_add_files_config_set_not_found(unit: ConfigSetService):
    # given
    files = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}

    # when / then
    with pytest.raises(ConfigSetNotFoundError):
        _ = unit.add_files(DEFAULT_CONFIG_SET_NAME, files)


def test_add_files_already_exists(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
):
    # given
    config_set_entry = ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path(DEFAULT_CONFIG_FILE_NAME))
    config_set = ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[config_set_entry])

    files = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}
    _ = repo.save(config_set)

    # when / then
    with pytest.raises(ConfigFileAlreadyExistsError):
        _ = unit.add_files(DEFAULT_CONFIG_SET_NAME, files)


def test_writes_file_bytes_correctly(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
    file_handler: ConfigSetFileHandlerMock
):
    # given
    _ = repo.save(ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[]))

    # when
    config_set = unit.add_files(DEFAULT_CONFIG_SET_NAME, {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES})

    # then
    assert file_handler.retrieve(config_set.files[0].id) == DEFAULT_CONFIG_FILE_BYTES


def test_file_writing_failure(
    unit: ConfigSetService,
    repo: ConfigSetRepositoryMock,
    file_handler: ConfigSetFileHandlerMock
):
    # given
    _ = repo.save(ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[]))
    files = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}

    # Simulate a failure in the file handler's store method
    def failing_store(ident: UUID, data: bytes, overwrite: bool = False) -> None:
        raise FileWriteError(str(ident), f"Simulated file writing failure: overwrite={overwrite} data={data}")

    file_handler.store = failing_store

    # when / then
    with pytest.raises(OperationFailedError, match="The operation 'add_files' failed. Reason: Simulated file writing failure"):
        _ = unit.add_files(DEFAULT_CONFIG_SET_NAME, files)


def test_add_files_empty_file_list(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given
    empty_files: dict[str, bytes] = {}
    _ = repo.save(ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[]))

    # when
    updated_config_set = unit.add_files(DEFAULT_CONFIG_SET_NAME, empty_files)

    # then
    assert len(updated_config_set.files) == 0


def test_correct_file_content(unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock):
    # given
    files = {DEFAULT_CONFIG_FILE_NAME: DEFAULT_CONFIG_FILE_BYTES}
    _ = repo.save(ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[]))

    # when
    config_set = unit.add_files(DEFAULT_CONFIG_SET_NAME, files)

    # then
    for entry in config_set.files:
        stored_bytes = file_handler.retrieve(entry.id)
        assert stored_bytes == files[str(entry.name)], f"Content mismatch for file {entry.name}"


@pytest.mark.parametrize("file_name", [
    "valid-file.txt",
    "another_valid_file.doc",
    "file_with_numbers_123.pdf",
    "file.name.with.dots.txt",
    "file-name_with-mixed_chars.txt",
    "file with spaces.txt",
    "file/with/full/name.txt",
    "win\\file\\with\\full\\name.txt",
])
def test_valid_file_names(unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_handler: ConfigSetFileHandlerMock, file_name: str):
    # given
    files = {file_name: DEFAULT_CONFIG_FILE_BYTES}
    _ = repo.save(ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[]))

    # when
    config_set = unit.add_files(DEFAULT_CONFIG_SET_NAME, files)

    # then
    assert len(config_set.files) == 1
    stored_bytes = file_handler.retrieve(config_set.files[0].id)
    assert stored_bytes == DEFAULT_CONFIG_FILE_BYTES


@pytest.mark.parametrize("file_name", [
    "invalid|file.doc",
    "invalid:file.doc",
    "invalid*file.doc",
    "invalid?file.doc",
    "invalid<file.doc",
    "invalid>file.doc",
    "invalid{file.doc",
    "invalid}file.doc",
    "invalid\"file.doc",
    "invalid!file.doc",
    "invalid$file.doc",
    "invalid%file.doc",
    "|:?<>{}\"!$%",
    "|invalid.doc",
    "invalid.doc|",
    ".",
    "invalid/",
    "invalid\\",
    "",
])
def test_invalid_file_names(unit: ConfigSetService, repo: ConfigSetRepositoryMock, file_name: str):
    # given
    files = {file_name: b"Sample content"}
    _ = repo.save(ConfigSet(name=DEFAULT_CONFIG_SET_NAME, files=[]))

    # when / then
    with pytest.raises(ConfigFileNameInvalidError):
        _ = unit.add_files(DEFAULT_CONFIG_SET_NAME, files)

