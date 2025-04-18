"""
Unit Test module.

This module contanis unit test for the packages in this repository. Unittests focus on the
functoinality of an individual component knows as the unit under test. Tests should be written
to test one thing and one thing only. Test names should be descriptive. Prefer long descriptive
names over short ambiguous ones.

Modules
-------

- tests.fixtures: Contains pytest.fixtures that are common to multiple unit tests.
- tests.mocks: Contains mock components that can be used to satisfy unit dependencies during tests.
- tests.helpers: Contain helpers such as constants, defaults, and factories to produce test data.


Example Unit Test File
----------------------

import pytest

from dflilb.service import SomeService

from tests.fixtures import *
from tests.mocks import *
from tests.helpers import *


@pytest.fixture
def unit(dependency_mock: SomeMock) -> SomeService:
    return SomeService(dependency_mock)


def test_unit_create_some_resource_in_dependency(unit: SomeService, dependency_mock: SomeMock):
    # given
    name = DEFAULT_NAME

    # when
    unit.do_something(name)

    # then
    assert dependency_mock.get_name() == name
"""
