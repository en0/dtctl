import pytest

from dflib.error import DuplicateConfigSetError, InvalidConfigSetNameError
from dflib.model import ConfigSet
from dflib.service import ConfigSetService
from tests.fixtures import *
from tests.helpers import *
from tests.mocks import *

from .fixtures import *


def test_can_create_config_set(
    unit: ConfigSetService, mock_config_set_repo: ConfigSetRepositoryMock
):
    # given
    name = DEFAULT_CONFIG_SET_NAME

    # when
    _ = unit.create(name)

    # then
    assert [m.name for m in mock_config_set_repo.find_all()] == [name]


def test_cannot_create_duplicate_config_set(
    unit: ConfigSetService, mock_config_set_repo: ConfigSetRepositoryMock
):
    # given
    name = DEFAULT_CONFIG_SET_NAME
    config_set = ConfigSet(name=name, files=[])
    _ = mock_config_set_repo.save(config_set)

    # when / then
    with pytest.raises(DuplicateConfigSetError):
        _ = unit.create(name)


def test_cannot_create_config_set_with_empty_name(unit: ConfigSetService):
    # given
    empty_name = ""

    # when / then
    with pytest.raises(InvalidConfigSetNameError):
        _ = unit.create(empty_name)


@pytest.mark.parametrize(
    "whitespace_name",
    [
        "   ",  # Spaces
        "\t",  # Tab
        "\n",  # Newline
        "\r",  # Carriage return
        "\r\n",  # Carriage return + Newline
        "\t\n",  # Tab + Newline
    ],
)
def test_cannot_create_config_set_with_whitespace_name(
    unit: ConfigSetService, whitespace_name: str
):
    # when / then
    with pytest.raises(InvalidConfigSetNameError):
        _ = unit.create(whitespace_name)


@pytest.mark.parametrize(
    "invalid_name",
    [
        "name!",  # Exclamation mark
        "name@",  # At symbol
        "name#",  # Hash
        "name$",  # Dollar sign
        "name%",  # Percent
        "name^",  # Caret
        "name&",  # Ampersand
        "name*",  # Asterisk
        "name(",  # Open parenthesis
        "name)",  # Close parenthesis
        "name+",  # Plus
        "name=",  # Equals
        "name{",  # Open brace
        "name}",  # Close brace
        "name[",  # Open bracket
        "name]",  # Close bracket
        "name|",  # Pipe
        "name\\",  # Backslash
        "name;",  # Semicolon
        "name'",  # Single quote
        'name"',  # Double quote
        "name<",  # Less than
        "name>",  # Greater than
        "name,",  # Comma
        "name?",  # Question mark
        "name/",  # Forward slash
    ],
)
def test_cannot_create_config_set_with_special_chars(unit: ConfigSetService, invalid_name: str):
    # when / then
    with pytest.raises(InvalidConfigSetNameError):
        _ = unit.create(invalid_name)


@pytest.mark.parametrize(
    "non_string_name",
    [
        [],  # Empty list
        {},  # Empty dictionary
        object(),  # Generic object
    ],
)
def test_cannot_create_config_set_with_non_stringable_name(
    unit: ConfigSetService, non_string_name: str
):
    # when / then
    with pytest.raises(InvalidConfigSetNameError):
        _ = unit.create(non_string_name)


@pytest.mark.parametrize(
    "untrimmed_whitespace",
    [
        " name",
        "\tname",
        "\rname",
        "\nname",
        "name ",
        "name\t",
        "name\r",
        "name\n",
        " name ",
        " name\t",
    ],
)
def test_can_trim_whitespace_in_config_set_name(
    unit: ConfigSetService,
    mock_config_set_repo: ConfigSetRepositoryMock,
    untrimmed_whitespace: str,
):
    # when
    _ = unit.create(untrimmed_whitespace)

    # then
    assert [m.name for m in mock_config_set_repo.find_all()] == ["name"]


def test_cannot_create_config_set_with_name_exceeding_max_length(unit: ConfigSetService):
    # given
    long_name = "a" * 26  # 26 characters

    # when / then
    with pytest.raises(InvalidConfigSetNameError):
        _ = unit.create(long_name)


def test_can_create_config_set_with_max_length_name(
    unit: ConfigSetService, repo: ConfigSetRepositoryMock
):
    # given
    max_length_name = "a" * 25  # 25 characters

    # when
    _ = unit.create(max_length_name)

    # then
    config_set = repo.find_by_id(max_length_name)
    assert config_set.name == max_length_name
