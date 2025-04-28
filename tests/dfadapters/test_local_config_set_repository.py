from pathlib import Path

import pytest

from dfadapter.config_set_repository import LocalConfigSetRepository, LocalConfigSetRepositoryConfig
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
