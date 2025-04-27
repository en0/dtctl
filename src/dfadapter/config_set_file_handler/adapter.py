from uuid import UUID

from dflib.typing import IConfigSetFileHandler

from .config import LocalConfigSetFileHandlerConfig


class LocalConfigSetFileHandler(IConfigSetFileHandler):

    def store(self, ident: UUID, data: bytes, overwrite: bool = False) -> None:
        raise NotImplementedError()

    def retrieve(self, ident: UUID) -> bytes:
        raise NotImplementedError()

    def remove(self, ident: UUID) -> None:
        raise NotImplementedError()

    def __init__(self, config: LocalConfigSetFileHandlerConfig):
        self.config: LocalConfigSetFileHandlerConfig = config
