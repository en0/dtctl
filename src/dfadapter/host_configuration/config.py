from pathlib import Path
from typing import NamedTuple


class LocalHostConfigurationOverrides(NamedTuple):
    section: str
    key: str
    value: str


class LocalHostConfigurationOpts(NamedTuple):
    rcfile: Path
    overrides: list[LocalHostConfigurationOverrides] | None = None
