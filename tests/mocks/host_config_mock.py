from typing import override

from dflib.typing.host_configuration import IHostConfiguration


class HostConfigMock(IHostConfiguration):

    @override
    def read_slist(self, section: str, key: str, default: list[str]) -> list[str]:
        val = self.config.get(section, {}).get(key, default)
        if isinstance(val, list) and all([isinstance(f, str) for f in val]):
            return [str(v) for v in val]
        return default

    @override
    def read_ilist(self, section: str, key: str, default: list[int]) -> list[int]:
        val = self.config.get(section, {}).get(key, default)
        if isinstance(val, list) and all([isinstance(f, int) for f in val]):
            return [int(v) for v in val]
        return default

    @override
    def read_str(self, section: str, key: str, default: str) -> str:
        val = self.config.get(section, {}).get(key, default)
        if isinstance(val, str):
            return val
        return default

    @override
    def read_int(self, section: str, key: str, default: int) -> int:
        val = self.config.get(section, {}).get(key, default)
        if isinstance(val, int):
            return val
        return default

    def set_config(self, config: dict[str, dict[str, str | int | list[str] | list[int]]]):
        self.config: dict[str, dict[str, str | int | list[str] | list[int]]] = config
