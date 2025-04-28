from logging import getLogger
from pathlib import Path
from typing import override
from uuid import UUID

from dflib.error import FileConflictError, FileReadError, FileWriteError
from dflib.typing import IConfigSetFileHandler

from .config import LocalConfigSetFileHandlerConfig

logger = getLogger(__name__)


class LocalConfigSetFileHandler(IConfigSetFileHandler):
    """A local filesystem implementation of the IConfigSetFileHandler interface.

    This class provides a concrete implementation of the IConfigSetFileHandler interface,
    facilitating the storage and retrieval of file data within a local filesystem. Each file is
    uniquely identified and stored in a directory specified by the 'fileStoreDirectory'
    configuration key within the 'ConfigSetFileHandler.LocalFS' section.

    For instance, if the 'fileStoreDirectory' is configured to '~/.config/dflib/files', and a file
    with the identifier '654a48df-dbb8-44dd-b2f0-09edf75ed148' is stored with the content 'b"hello,
    world"', the file with that content will be created at:

    ~/.config/dflib/files/654a48df-dbb8-44dd-b2f0-09edf75ed148

    The class ensures that the necessary directory structure is created if it does not already
    exist.
    """

    @override
    def store(self, ident: UUID, data: bytes, overwrite: bool = False) -> None:

        target = self.file_store_dir / str(ident)

        try:
            self.file_store_dir.mkdir(parents=True, exist_ok=True)
            if not overwrite and target.exists():
                raise FileConflictError(str(target), "Unable to write file. File exists.")

            _ = target.write_bytes(data)

        except OSError as ex:
            logger.exception("Failed to write %s due to unexpected OSError", target)
            raise FileWriteError(str(target), "Unexpected OSError") from ex

    @override
    def retrieve(self, ident: UUID) -> bytes:

        target = self.file_store_dir / str(ident)

        try:
            return target.read_bytes()

        except FileNotFoundError as ex:
            raise FileReadError(str(target), str(ex))

        except OSError as ex:
            logger.exception("Failed to read %s due to unexpected OSError", target)
            raise FileReadError(str(target), "Unexpected OSError") from ex

    @override
    def remove(self, ident: UUID) -> None:

        target = self.file_store_dir / str(ident)

        try:
            target.unlink()

        except FileNotFoundError as ex:
            raise FileWriteError(str(target), str(ex))

        except OSError as ex:
            logger.exception("Failed to remove %s due to unexpected OSError", target)
            raise FileWriteError(str(target), "Unexpected OSError") from ex

    def __init__(self, config: LocalConfigSetFileHandlerConfig):
        self.file_store_dir: Path = config.file_store_dir
