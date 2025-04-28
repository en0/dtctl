from pathlib import Path
from typing import override

from dflib.adapter.config import AdapterConfigABC


class LocalConfigSetFileHandlerConfig(AdapterConfigABC):

    @property
    @override
    def section(self) -> str:
        return "ConfigSetFileHandler.LocalFS"

    @property
    def file_store_dir(self) -> Path:
        path = self.read_str("fileStoreDirectory", "~/.config/dflib/files")
        return Path(path)
