from pathlib import Path
from typing import override

from dflib.adapter.config import AdapterConfigABC


class LocalConfigSetRepositoryConfig(AdapterConfigABC):

    @property
    @override
    def section(self) -> str:
        return "ConfigSetRepository.LocalFS"

    @property
    def catalog_path(self) -> Path:
        path = self.read_str("catalogPath", "~/.config/dflib/catalog")
        return Path(path)
