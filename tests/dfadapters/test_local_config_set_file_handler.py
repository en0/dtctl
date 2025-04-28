from pathlib import Path

import pytest

from dfadapter.config_set_file_handler import (
    LocalConfigSetFileHandler,
    LocalConfigSetFileHandlerConfig,
)
from dflib.error import FileConflictError, FileReadError, FileWriteError
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *


@pytest.fixture
def file_path(tmp_path: Path):
    return tmp_path / "files"


@pytest.fixture
def unit(host_config: HostConfigMock, file_path: Path):
    host_config.set_config(
        {
            "ConfigSetFileHandler.LocalFS": {
                "fileStoreDirectory": str(file_path),
            }
        }
    )
    config = LocalConfigSetFileHandlerConfig(host_config)
    return LocalConfigSetFileHandler(config)


def test_can_create_local_file_config_handler(unit: LocalConfigSetFileHandler):
    # given: a unit to test
    # when/then: it's a valid class.
    assert isinstance(unit, LocalConfigSetFileHandler)


def test_file_path_gets_created_on_save_operation_if_not_exists(
    unit: LocalConfigSetFileHandler, file_path: Path
):
    # given: file_path does not exist
    assert file_path.exists() == False

    # when: calling store on unit
    unit.store(DEFAULT_FILE_IDENTITY, DEFAULT_CONFIG_FILE_BYTES)

    # then: file_path should now exist
    assert file_path.exists()


def test_store_creates_file_in_file_path(unit: LocalConfigSetFileHandler, file_path: Path):
    # given: target file doesn't exist
    target = file_path / str(DEFAULT_FILE_IDENTITY)

    # when: writing new file
    unit.store(DEFAULT_FILE_IDENTITY, DEFAULT_CONFIG_FILE_BYTES)

    # then: target file exists
    assert target.exists()


def test_store_write_bytes_into_file(unit: LocalConfigSetFileHandler, file_path: Path):
    # given: target file doesn't exist
    target = file_path / str(DEFAULT_FILE_IDENTITY)

    # when: writing new file
    unit.store(DEFAULT_FILE_IDENTITY, DEFAULT_CONFIG_FILE_BYTES)

    # then: target file contains bytes
    assert target.read_bytes() == DEFAULT_CONFIG_FILE_BYTES


def test_store_riases_conflict_error_when_file_exists(
    unit: LocalConfigSetFileHandler, file_path: Path
):
    # given: target file already exists
    file_path.mkdir(parents=True, exist_ok=True)
    target = file_path / str(DEFAULT_FILE_IDENTITY)
    _ = target.write_bytes(DEFAULT_CONFIG_FILE_BYTES)

    # when: writing new file
    # then: raises FileConflictError
    with pytest.raises(FileConflictError):
        unit.store(DEFAULT_FILE_IDENTITY, DEFAULT_CONFIG_FILE_BYTES)


def test_store_doesnt_change_file_if_conflict(unit: LocalConfigSetFileHandler, file_path: Path):
    # given: target file already exists
    altered_content = DEFAULT_CONFIG_FILE_BYTES + b"hello_world"
    file_path.mkdir(parents=True, exist_ok=True)
    target = file_path / str(DEFAULT_FILE_IDENTITY)
    _ = target.write_bytes(DEFAULT_CONFIG_FILE_BYTES)

    # when: writing new file cases FileConflictError
    with pytest.raises(FileConflictError):
        unit.store(DEFAULT_FILE_IDENTITY, altered_content)

    # then: the file is unchanged
    assert target.read_bytes() == DEFAULT_CONFIG_FILE_BYTES


def test_store_writes_file_when_exists_if_overwrite(
    unit: LocalConfigSetFileHandler, file_path: Path
):
    # given: target file already exists
    altered_content = DEFAULT_CONFIG_FILE_BYTES + b"hello_world"
    file_path.mkdir(parents=True, exist_ok=True)
    target = file_path / str(DEFAULT_FILE_IDENTITY)
    _ = target.write_bytes(DEFAULT_CONFIG_FILE_BYTES)

    # when: writing new file with overwrite flag set
    unit.store(DEFAULT_FILE_IDENTITY, altered_content, overwrite=True)

    # then: updates the file
    assert target.read_bytes() == altered_content


def test_retrieve_can_read_existing_file(unit: LocalConfigSetFileHandler, file_path: Path):
    # given: target file exists
    file_path.mkdir(parents=True, exist_ok=True)
    target = file_path / str(DEFAULT_FILE_IDENTITY)
    _ = target.write_bytes(DEFAULT_CONFIG_FILE_BYTES)

    # when: reading file bytes
    result = unit.retrieve(DEFAULT_FILE_IDENTITY)

    # then: the content matches expected
    assert result == DEFAULT_CONFIG_FILE_BYTES


def test_retrieve_raises_file_read_error_if_file_path_no_exist(
    unit: LocalConfigSetFileHandler, file_path: Path
):
    # given: file_path doesn't exist
    assert not file_path.exists()

    # when: reading file bytes
    # then: raises FileReadError
    with pytest.raises(FileReadError):
        _ = unit.retrieve(DEFAULT_FILE_IDENTITY)


def test_retrieve_raises_file_read_error_if_file_no_exists(
    unit: LocalConfigSetFileHandler, file_path: Path
):
    # given: file_path exists, but file doesn't exist
    file_path.mkdir(parents=True, exist_ok=True)

    # when: reading file bytes
    # then: raises FileReadError
    with pytest.raises(FileReadError):
        _ = unit.retrieve(DEFAULT_FILE_IDENTITY)


def test_remove_can_remove_file(unit: LocalConfigSetFileHandler, file_path: Path):
    # given: file exists.
    file_path.mkdir(parents=True, exist_ok=True)
    target = file_path / str(DEFAULT_FILE_IDENTITY)
    _ = target.write_bytes(DEFAULT_CONFIG_FILE_BYTES)

    # when: asked to remove file
    unit.remove(DEFAULT_FILE_IDENTITY)

    # then: file no longer exists
    assert not target.exists()


def test_remove_raises_file_write_error_if_file_path_no_exist(
    unit: LocalConfigSetFileHandler, file_path: Path
):
    # given: file_path doesn't exists.
    assert not file_path.exists()

    # when: asked to remove file
    # then: unit raises FileWriteError
    with pytest.raises(FileWriteError):
        unit.remove(DEFAULT_FILE_IDENTITY)


def test_remove_raises_file_write_error_if_file_no_exist(
    unit: LocalConfigSetFileHandler, file_path: Path
):
    # given: file_path exists, but file doesn't exist
    file_path.mkdir(parents=True, exist_ok=True)

    # when: asked to remove file
    # then: unit raises FileWriteError
    with pytest.raises(FileWriteError):
        unit.remove(DEFAULT_FILE_IDENTITY)
