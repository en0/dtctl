from pathlib import Path

import pytest

from dfadapter.config_set_file_handler import (
    LocalConfigSetFileHandler,
    LocalConfigSetFileHandlerConfig,
)
from dflib.typing.host_configuration import IHostConfiguration
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *


@pytest.fixture
def unit(host_config: HostConfigMock, request):
    if hasattr(request, "param"):
        host_config.set_config(request.param)
    else:
        host_config.set_config({"ConfigSetFileHandler.LocalFS": {}})
    config = LocalConfigSetFileHandlerConfig(host_config)
    return LocalConfigSetFileHandler(config)


def test_can_create_local_file_config_handler(unit: LocalConfigSetFileHandler):
    # given: a unit to test
    # when/then: it's a valid class.
    assert isinstance(unit, LocalConfigSetFileHandler)
