import json
from configparser import ConfigParser
from logging import getLogger
from pathlib import Path
from typing import override

from pyioc3.autowire import bind

from dflib.error import ConfigurationValueError
from dflib.typing.host_configuration import IHostConfiguration

from .config import LocalHostConfigurationOpts

logger = getLogger(__name__)


@bind(IHostConfiguration, scope="SINGLETON")
class LocalHostConfiguration(IHostConfiguration):

    @override
    def read_slist(self, section: str, key: str, default: list[str]) -> list[str]:
        try:
            val = json.loads(self._get_value(section, key))
            return [str(i) for i in val]
        except KeyError:
            return default
        except (json.JSONDecodeError, TypeError, ValueError):
            raise ConfigurationValueError(
                f"{section}.{key}", self._conf[section][key], "list[string]"
            )

    @override
    def read_ilist(self, section: str, key: str, default: list[int]) -> list[int]:
        try:
            val = json.loads(self._get_value(section, key))
            return [int(i) for i in val]
        except KeyError:
            return default
        except (json.JSONDecodeError, TypeError, ValueError):
            raise ConfigurationValueError(
                f"{section}.{key}", self._conf[section][key], "list[integer]"
            )

    @override
    def read_str(self, section: str, key: str, default: str) -> str:
        try:
            val = self._get_value(section, key)
            return str(val)
        except KeyError:
            return default
        except ValueError:
            raise ConfigurationValueError(f"{section}.{key}", self._conf[section][key], "string")

    @override
    def read_int(self, section: str, key: str, default: int) -> int:
        try:
            val = self._get_value(section, key)
            return int(val)
        except KeyError:
            return default
        except ValueError:
            raise ConfigurationValueError(f"{section}.{key}", self._conf[section][key], "integer")

    @override
    def set_override(self, section: str, key: str, value: str) -> None:
        key = f"{section}:{key}"
        self._overrides[key] = value

    def _get_value(self, section: str, key: str) -> str:
        override_key = f"{section}:{key}"
        if override_key in self._overrides:
            return self._overrides[override_key]
        else:
            return self._conf[section][key]

    def __init__(self, opts: LocalHostConfigurationOpts):
        self._overrides: dict[str, str] = {}
        self._conf: ConfigParser = ConfigParser()
        rcfile = Path.expanduser(opts.rcfile)
        if rcfile.exists():
            with rcfile.open("r") as fd:
                self._conf.read_file(fd)
        for o in opts.overrides or []:
            self.set_override(o.section, o.key, o.value)
