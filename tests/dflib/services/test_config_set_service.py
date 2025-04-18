import pytest

from dflib.error import DuplicateConfigSetError
from dflib.service import ConfigSetService
from dflib.typing import IRepository, IConfigSetFileHandler
from dflib.model import ConfigSet

from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *


@pytest.fixture
def unit(
    mock_config_set_repo: IRepository[ConfigSet, str],
    config_set_file_handler: IConfigSetFileHandler,
) -> ConfigSetService:
    """
    Fixture for the ConfigSetService, initialized with mocked dependencies.
    """
    return ConfigSetService(mock_config_set_repo, config_set_file_handler)


def test_can_create_instance_of_config_set_service(unit: ConfigSetService):
    assert unit


def test_can_create_config_set(
    unit: ConfigSetService,
    mock_config_set_repo: ConfigSetRepositoryMock
):
    # given
    name = DEFAULT_CONFIG_SET_NAME

    # when
    _ = unit.create(name)

    # then
    assert [m.name for m in mock_config_set_repo.find_all()] == [name]


def test_cannot_create_duplicate_config_set(
    unit: ConfigSetService,
    mock_config_set_repo: ConfigSetRepositoryMock
):
    # given
    name = DEFAULT_CONFIG_SET_NAME
    config_set = ConfigSet(name=name, files=[])
    _ = mock_config_set_repo.save(config_set)

    # when / then
    with pytest.raises(DuplicateConfigSetError):
        _ = unit.create(name)
