from abc import ABC, abstractmethod


class IHostConfiguration(ABC):
    """
    Interface for managing host configuration settings.

    This interface defines methods for accessing configuration values
    from a specified section. Implementations must provide concrete
    methods for reading lists and individual values of strings and
    integers.

    Responsibilities:
        - Abstract access to configuration data.
        - Provide methods to read string and integer values, both as
          individual items and lists.
        - Handle default values when configuration keys are missing.

    Methods:
        - `read_slist(section: str, key: str, default: list[str]) -> list[str]`:
          Read a list of strings from the configuration.
        - `read_ilist(section: str, key: str, default: list[int]) -> list[int]`:
          Read a list of integers from the configuration.
        - `read_str(section: str, key: str, default: str) -> str`:
          Read a string from the configuration.
        - `read_int(section: str, key: str, default: int) -> int`:
          Read an integer from the configuration.

    Exception Handling:
        - Implementations should handle exceptions related to missing
          configuration sections or keys, and provide meaningful
          defaults or error messages.
    """

    @abstractmethod
    def read_slist(self, section: str, key: str, default: list[str]) -> list[str]:
        """
        Read a list of strings from the specified configuration section.

        Args:
            section (str): The configuration section to read from.
            key (str): The configuration key to read.
            default (list[str]): The default value to return if the key is not found.

        Returns:
            list[str]: The list of strings from the configuration, or the default value.
        """
        raise NotImplementedError()

    @abstractmethod
    def read_ilist(self, section: str, key: str, default: list[int]) -> list[int]:
        """
        Read a list of integers from the specified configuration section.

        Args:
            section (str): The configuration section to read from.
            key (str): The configuration key to read.
            default (list[int]): The default value to return if the key is not found.

        Returns:
            list[int]: The list of integers from the configuration, or the default value.
        """
        raise NotImplementedError()

    @abstractmethod
    def read_str(self, section: str, key: str, default: str) -> str:
        """
        Read a string from the specified configuration section.

        Args:
            section (str): The configuration section to read from.
            key (str): The configuration key to read.
            default (str): The default value to return if the key is not found.

        Returns:
            str: The string from the configuration, or the default value.
        """
        raise NotImplementedError()

    @abstractmethod
    def read_int(self, section: str, key: str, default: int) -> int:
        """
        Read an integer from the specified configuration section.

        Args:
            section (str): The configuration section to read from.
            key (str): The configuration key to read.
            default (int): The default value to return if the key is not found.

        Returns:
            int: The integer from the configuration, or the default value.
        """
        raise NotImplementedError()
