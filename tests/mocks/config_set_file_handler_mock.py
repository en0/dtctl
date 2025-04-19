from dflib.error import FileConflictError
from dflib.typing import IConfigSetFileHandler
from uuid import UUID
from typing import override


class ConfigSetFileHandlerMock(IConfigSetFileHandler):

    @override
    def store(self, ident: UUID, data: bytes, overwrite: bool = False) -> None:
        if not overwrite and ident in self.storage:
            raise FileConflictError(f"File with UUID {ident} already exists.")
        self.storage[ident] = data

    @override
    def retrieve(self, ident: UUID) -> bytes:
        if ident not in self.storage:
            raise FileNotFoundError(f"File with UUID {ident} not found.")
        return self.storage[ident]

    @override
    def remove(self, ident: UUID) -> None:
        if ident not in self.storage:
            raise FileNotFoundError(f"File with UUID {ident} not found.")
        del self.storage[ident]

    def __init__(self):
        self.storage: dict[UUID, bytes]  = {}
