from typing import override

import pytest

from dflib.adapter.config import AdapterConfigABC
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *


class AdapterConfigImpl(AdapterConfigABC):

    @property
    @override
    def section(self) -> str:
        return "Unit.test"


@pytest.fixture
def unit(host_config: HostConfigMock, request):
    host_config.set_config(request.param)
    return AdapterConfigImpl(host_config)


@pytest.mark.parametrize("unit", [{"Unit.test": {}}], indirect=True)
def test_get_section(unit: AdapterConfigImpl):
    assert unit.section == "Unit.test"


@pytest.mark.parametrize("unit", [{"Unit.test": {"foo": 123}}], indirect=True)
def test_get_int(unit: AdapterConfigImpl):
    assert unit.read_int("foo", 321) == 123


@pytest.mark.parametrize("unit", [{"Unit.test": {"foo": "123"}}], indirect=True)
def test_get_str(unit: AdapterConfigImpl):
    assert unit.read_str("foo", "321") == "123"


@pytest.mark.parametrize("unit", [{"Unit.test": {"foo": [123, 345]}}], indirect=True)
def test_get_ilist(unit: AdapterConfigImpl):
    assert unit.read_ilist("foo", [321, 543]) == [123, 345]


@pytest.mark.parametrize("unit", [{"Unit.test": {"foo": ["123", "345"]}}], indirect=True)
def test_get_slist(unit: AdapterConfigImpl):
    assert unit.read_slist("foo", ["321", "543"]) == ["123", "345"]


@pytest.mark.parametrize("unit", [{"Unit.test": {}}], indirect=True)
def test_get_int_default(unit: AdapterConfigImpl):
    assert unit.read_int("foo", 321) == 321


@pytest.mark.parametrize("unit", [{"Unit.test": {}}], indirect=True)
def test_get_str_default(unit: AdapterConfigImpl):
    assert unit.read_str("foo", "321") == "321"


@pytest.mark.parametrize("unit", [{"Unit.test": {}}], indirect=True)
def test_get_ilist_default(unit: AdapterConfigImpl):
    assert unit.read_ilist("foo", [321, 543]) == [321, 543]


@pytest.mark.parametrize("unit", [{"Unit.test": {}}], indirect=True)
def test_get_slist_default(unit: AdapterConfigImpl):
    assert unit.read_slist("foo", ["321", "543"]) == ["321", "543"]
