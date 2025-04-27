from typing import Any
from unittest.mock import MagicMock

import pytest

from dflib.model import ConfigSet
from dflib.typing import IConfigSetFileHandler, IRepository
from dflib.typing.host_configuration import IHostConfiguration
from tests.mocks import ConfigSetFileHandlerMock, ConfigSetRepositoryMock, HostConfigMock


@pytest.fixture
def host_config() -> IHostConfiguration:
    """
    Mock implementation of IHostConfiguration.
    """
    return HostConfigMock()


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
