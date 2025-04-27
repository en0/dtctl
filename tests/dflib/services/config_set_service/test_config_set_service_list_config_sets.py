import pytest

from dflib.error import OperationFailedError, QueryExecutionError
from dflib.service import ConfigSetService
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *

from .fixtures import *


def test_list_config_sets_with_no_sets(unit: ConfigSetService):
    # given: no configuration sets exist in the repository

    # when: listing all configuration sets
    config_sets = unit.list_config_sets()

    # then: an empty list is returned
    assert config_sets == []


def test_list_config_sets_with_single_set(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: a single configuration set exists in the repository
    _ = repo.save(ConfigSet(DEFAULT_CONFIG_SET_NAME, []))

    # when: listing all configuration sets
    config_sets = unit.list_config_sets()

    # then: a list containing the single configuration set name is returned
    assert config_sets == [DEFAULT_CONFIG_SET_NAME]


def test_list_config_sets_with_multiple_sets(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: multiple configuration sets exist in the repository
    _ = repo.save(ConfigSet("config_set_1", []))
    _ = repo.save(ConfigSet("config_set_2", []))
    _ = repo.save(ConfigSet("config_set_3", []))

    # when: listing all configuration sets
    config_sets = unit.list_config_sets()

    # then: a list containing all configuration set names is returned
    assert config_sets == ["config_set_1", "config_set_2", "config_set_3"]


def test_list_config_raises_operation_error(unit: ConfigSetService, repo: ConfigSetRepositoryMock):
    # given: the repository raises a QueryExecutionError
    def raise_error(*_):
        raise QueryExecutionError("unit test", "database error")

    repo.find_all = raise_error

    # when: attempting to list configuration sets
    # then: OperationFailedError is raised
    with pytest.raises(OperationFailedError):
        _ = unit.list_config_sets()
