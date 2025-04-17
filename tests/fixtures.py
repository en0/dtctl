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
    return RepositoryMock[ConfigSet, str]()


@pytest.fixture
def config_set_file_handler() -> IConfigSetFileHandler:
    """
    Mock implementation of IConfigSetFileHandler.
    """
    return MagicMock(spec=IConfigSetFileHandler)
