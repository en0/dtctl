import pytest

from dflib.model import ConfigSet
from dflib.typing import IRepository, IConfigSetFileHandler
from unittest.mock import MagicMock


from tests.mocks import *


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
