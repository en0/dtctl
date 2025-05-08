from typing import override

from dfadapter.host_configuration.config import LocalHostConfigurationOverrides


class Variant:

    def as_override(self) -> LocalHostConfigurationOverrides:
        return LocalHostConfigurationOverrides(self.section, self.key, self.value)

    def __init__(self, override_str: str):
        section, part = override_str.split(":", 2)
        key, value = part.split("=", 2)
        self.section: str = section
        self.key: str = key
        self.value: str = value

    @override
    def __repr__(self) -> str:
        return f"{self.section}:{self.key}={self.value}"
