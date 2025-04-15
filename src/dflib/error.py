"""All exception classes for dflib"""


class DFLibError(Exception):
    """Base class for all exceptions raised by dflib."""
    pass


class FileReadError(DFLibError):
    """
    Exception raised when there is an issue reading a file.

    This exception is intended to capture errors that occur while attempting to access or read a
    file.

    Attributes:
        file_path (str): The path of the file that could not be read.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "Unable to read file."):
        super().__init__(message)
        self.file_path: str = file_path


class FileNotFoundError(FileReadError):
    """
    Exception raised when a read operation is attempted against a non-existant file path.

    This exception is a specialized form of `FileReadError` and is intended to capture cases where a
    file read operation fails because the source file does not exist.

    Attributes:
        file_path (str): The path of the file that caused the conflict.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "Unable to write file due to conflict."):
        super().__init__(message)
        self.file_path: str = file_path



class FileWriteError(DFLibError):
    """
    Exception raised when there is an issue writing a file.

    This exception is intended to capture errors that occur while attempting to write data to a
    file.

    Attributes:
        file_path (str): The path of the file that could not be written.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "Unable to write file."):
        super().__init__(message)
        self.file_path: str = file_path


class FileConflictError(FileWriteError):
    """
    Exception raised when there is a conflict while attempting to write a file.

    This exception is a specialized form of `FileWriteError` and is intended to capture cases where
    a file write operation fails due to a conflict. For example, this might occur if the file
    already exists and overwriting is not allowed.

    Attributes:
        file_path (str): The path of the file that caused the conflict.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, file_path: str, message: str = "Unable to write file due to conflict."):
        super().__init__(message)
        self.file_path: str = file_path

