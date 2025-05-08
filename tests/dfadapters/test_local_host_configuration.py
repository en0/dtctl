from pathlib import Path

import pytest

from dfadapter.host_configuration import LocalHostConfiguration, LocalHostConfigurationOpts
from dflib.error import ConfigurationValueError


@pytest.fixture
def conf_path(tmp_path: Path):
    return tmp_path / "config"


@pytest.fixture
def unit(conf_path: Path, request) -> LocalHostConfiguration:
    if hasattr(request, "param"):
        with conf_path.open("w") as fd:
            _ = fd.write(request.param)
    opts = LocalHostConfigurationOpts(rcfile=conf_path)
    return LocalHostConfiguration(opts)


def test_can_create_instance(unit: LocalHostConfiguration):
    assert isinstance(unit, LocalHostConfiguration)


@pytest.mark.parametrize("unit", ["[MySection]\nfoo=bar"], indirect=True)
def test_can_read_string_setting(unit: LocalHostConfiguration):
    assert unit.read_str("MySection", "foo", "baz") == "bar"


def test_get_string_default_if_variable_not_set(unit: LocalHostConfiguration):
    assert unit.read_str("MySection", "foo", "baz") == "baz"


@pytest.mark.parametrize("unit", ["[MySection]\nfoo=42"], indirect=True)
def test_can_read_int_setting(unit: LocalHostConfiguration):
    assert unit.read_int("MySection", "foo", 0) == 42


def test_get_int_default_if_variable_not_set(unit: LocalHostConfiguration):
    assert unit.read_int("MySection", "foo", 0) == 0


@pytest.mark.parametrize("unit", ['[MySection]\nfoo=["hello"]'], indirect=True)
def test_can_read_slist_setting(unit: LocalHostConfiguration):
    assert unit.read_slist("MySection", "foo", []) == ["hello"]


def test_get_slist_default_if_variable_not_set(unit: LocalHostConfiguration):
    assert unit.read_slist("MySection", "foo", []) == []


@pytest.mark.parametrize("unit", ["[MySection]\nfoo=[42]"], indirect=True)
def test_can_read_ilist_setting(unit: LocalHostConfiguration):
    assert unit.read_ilist("MySection", "foo", []) == [42]


def test_get_ilist_default_if_variable_not_set(unit: LocalHostConfiguration):
    assert unit.read_slist("MySection", "foo", []) == []


@pytest.mark.parametrize("unit", ["[MySection]\nfoo=bar"], indirect=True)
def test_read_int_raises_config_error_if_value_cannot_be_converted_to_type(
    unit: LocalHostConfiguration,
):
    with pytest.raises(ConfigurationValueError):
        _ = unit.read_int("MySection", "foo", 0)


@pytest.mark.parametrize("unit", ["[MySection]\nfoo=bar"], indirect=True)
def test_read_ilist_raises_config_error_if_value_is_not_json_parsable(unit: LocalHostConfiguration):
    with pytest.raises(ConfigurationValueError):
        _ = unit.read_ilist("MySection", "foo", [])


@pytest.mark.parametrize("unit", ['[MySection]\nfoo=["hello"]'], indirect=True)
def test_read_ilist_raises_config_error_if_value_is_not_a_list_of_ints(
    unit: LocalHostConfiguration,
):
    with pytest.raises(ConfigurationValueError):
        _ = unit.read_ilist("MySection", "foo", [])


@pytest.mark.parametrize("unit", ["[MySection]\nfoo=42"], indirect=True)
def test_read_ilist_raises_config_error_if_value_is_not_a_list(unit: LocalHostConfiguration):
    with pytest.raises(ConfigurationValueError):
        _ = unit.read_ilist("MySection", "foo", [])


@pytest.mark.parametrize("unit", ["[MySection]\nfoo=42"], indirect=True)
def test_can_override_int(unit: LocalHostConfiguration):
    unit.set_override("MySection", "foo", "100")
    assert unit.read_int("MySection", "foo", 0) == 100
