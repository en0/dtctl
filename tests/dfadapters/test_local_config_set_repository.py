from configparser import ConfigParser
from pathlib import Path
from uuid import uuid4

import pytest

from dfadapter.config_set_repository import LocalConfigSetRepository, LocalConfigSetRepositoryConfig
from dflib.error import DuplicateEntityError, EntityNotFoundError
from dflib.model import ConfigSetEntry
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *


@pytest.fixture
def catalog_path(tmp_path: Path):
    return tmp_path / "catalog"


@pytest.fixture
def unit(host_config: HostConfigMock, catalog_path: Path) -> LocalConfigSetRepository:
    host_config.set_config(
        {
            "ConfigSetRepository.LocalFS": {
                "catalogPath": str(catalog_path),
            }
        }
    )
    config = LocalConfigSetRepositoryConfig(host_config)
    return LocalConfigSetRepository(config)


def test_can_create_local_file_config_handler(unit: LocalConfigSetRepository):
    # given: a unit to test
    # when/then: it's a valid class.
    assert isinstance(unit, LocalConfigSetRepository)


def test_add_config_creates_catalog_file(
    unit: LocalConfigSetRepository, catalog_path: Path
) -> None:
    # Given: The catalog doesn't exist
    assert not catalog_path.exists()
    config_set = ConfigSet("foo", [])

    # When: saving a new configset
    _ = unit.save(config_set)

    # Then: The catalog is created
    assert catalog_path.exists()


def test_can_add_config(unit: LocalConfigSetRepository, catalog_path: Path) -> None:
    # Given: A basic configset
    cp = ConfigParser()
    config_set = ConfigSet("foo", [])

    # When: Saved to the repo
    _ = unit.save(config_set)

    # Then: Configset exists in the catalog
    cp.read_string(catalog_path.read_text())
    assert cp.has_section("foo")
    assert len(cp["foo"]) == 0


def test_configset_files_are_correct(unit: LocalConfigSetRepository, catalog_path: Path) -> None:
    # Given: A basic configset
    cp = ConfigParser()
    config_set = ConfigSet("foo", [ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path(DEFAULT_FILE_PATH))])

    # When: Saved to the repo
    _ = unit.save(config_set)

    # Then: Configset exists in the catalog
    cp.read_string(catalog_path.read_text())
    assert len(cp["foo"]) == 1
    assert cp["foo"][str(config_set.files[0].name)] == str(config_set.files[0].id)


def test_duplicate_entry_error(unit: LocalConfigSetRepository) -> None:
    # Given: A basic configset that is already saved
    config_set = unit.save(ConfigSet("foo", []))

    # When/Then: Saved to the repo will raise a duplication error
    with pytest.raises(DuplicateEntityError):
        _ = unit.save(config_set)


def test_can_update_configset_add_files(unit: LocalConfigSetRepository, catalog_path: Path) -> None:
    # Given: A basic configset that is already saved
    cp = ConfigParser()
    config_set = unit.save(ConfigSet("foo", []))

    # When: updating the configset with a new file added
    config_set.files.append(ConfigSetEntry(DEFAULT_FILE_IDENTITY, Path(DEFAULT_FILE_PATH)))
    _ = unit.update(config_set)

    # Then: catalog has new file.
    cp.read_string(catalog_path.read_text())
    assert len(cp["foo"]) == 1
    assert cp["foo"][str(config_set.files[0].name)] == str(config_set.files[0].id)


def test_entity_not_found_error_on_update(unit: LocalConfigSetRepository) -> None:
    # Given: No config exists
    config_set = ConfigSet("foo", [])

    # When/Then: update the configset riases not found error
    with pytest.raises(EntityNotFoundError):
        _ = unit.update(config_set)


def test_can_delete_config(unit: LocalConfigSetRepository, catalog_path: Path) -> None:
    # Given: A basic configset that is already saved
    cp = ConfigParser()
    config_set = unit.save(ConfigSet("foo", []))

    # When: delete configset
    unit.delete(config_set.name)

    # Then: ConfigSet is deleted
    cp.read_string(catalog_path.read_text())
    assert not cp.has_section("foo")


def test_entity_not_found_error_on_delete(unit: LocalConfigSetRepository) -> None:
    # Given: No config exists
    config_set = ConfigSet("foo", [])

    # When/Then: delete the configset riases not found error
    with pytest.raises(EntityNotFoundError):
        _ = unit.delete(config_set.name)


def test_can_retreive_configset_by_name(unit: LocalConfigSetRepository) -> None:
    # Given: A basic configset that is already saved
    _ = unit.save(ConfigSet("foo", []))

    # When: retrieve configset
    config_set = unit.find_by_id("foo")

    # Then: configset should be correct
    assert config_set.name == "foo"
    assert len(config_set.files) == 0


def test_can_retreive_configset_by_name_raises_not_found(unit: LocalConfigSetRepository) -> None:
    # Given: No configset exists

    # When/Then: retrieve raises error
    with pytest.raises(EntityNotFoundError):
        _ = unit.find_by_id("foo")


def test_can_find_all_configsets(unit: LocalConfigSetRepository) -> None:
    # Given: A couple configs already saved
    _ = unit.save(ConfigSet("foo", []))
    _ = unit.save(ConfigSet("bar", []))

    # When: retrieve all
    config_sets = unit.find_all()

    # Then: all configsets are retrieved
    assert sorted([cs.name for cs in config_sets]) == ["bar", "foo"]
