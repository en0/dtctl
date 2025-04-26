import pytest

from dflib.model import ConfigSet
from dflib.typing import IConfigSetFileHandler, IRepository
from tests.mocks import ConfigSetFileHandlerMock, ConfigSetRepositoryMock


@pytest.fixture
def mock_config_set_repo() -> IRepository[ConfigSet, str]:
    """
    Mock implementation of IRepository for ConfigSet objects.
    """
    return ConfigSetRepositoryMock()


@pytest.fixture
def config_set_file_handler() -> IConfigSetFileHandler:
    """
    Mock implementation of IConfigSetFileHandler.
    """
    return ConfigSetFileHandlerMock()
