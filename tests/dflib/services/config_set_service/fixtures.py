import pytest

from dflib.model import ConfigSet
from dflib.service import ConfigSetService
from dflib.typing import IConfigSetFileHandler, IRepository


@pytest.fixture
def repo(mock_config_set_repo: IRepository[ConfigSet, str]) -> IRepository[ConfigSet, str]:
    return mock_config_set_repo


@pytest.fixture
def file_handler(config_set_file_handler: IConfigSetFileHandler) -> IConfigSetFileHandler:
    return config_set_file_handler


@pytest.fixture
def unit(
    repo: IRepository[ConfigSet, str],
    file_handler: IConfigSetFileHandler,
) -> ConfigSetService:
    """
    Fixture for the ConfigSetService, initialized with mocked dependencies.
    """
    return ConfigSetService(repo, file_handler)
