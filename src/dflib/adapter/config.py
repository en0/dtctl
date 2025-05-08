from abc import abstractmethod

from dflib.typing import IHostConfiguration


class AdapterConfigABC:
    """
    Abstract base class for managing adapter configuration settings.

    This class provides a common interface for reading configuration values
    from a host configuration. Subclasses must implement the `section` property
    to specify the configuration section they operate on.

    Responsibilities:
        - Provide a unified interface for accessing configuration data.
        - Define methods to read string and integer values, both as individual
          items and lists, from a specified configuration section.
        - Ensure that subclasses specify the configuration section they handle.

    Methods:
        - `section() -> str`: Abstract property to define the configuration section.
        - `read_slist(key: str, default: list[str]) -> list[str]`:
          Read a list of strings from the configuration.
        - `read_ilist(key: str, default: list[int]) -> list[int]`:
          Read a list of integers from the configuration.
        - `read_str(key: str, default: str) -> str`:
          Read a string from the configuration.
        - `read_int(key: str, default: int) -> int`:
          Read an integer from the configuration.

    Exception Handling:
        - Implementations should allow ConfigurationValueError to bubble up to the
          UI so it can provide feedback to the users.

    Example:
        class MyAdapterConfig(AdapterConfigABC):

            @property
            def section(self) -> str:
                return "ConfigSetFileHandler.MyAdapter"

            def my_int_variable(self) -> int:
                return self.read_int("myIntVariable", 42)
    """

    @property
    @abstractmethod
    def section(self) -> str:
        """
        The configuration section name.

        Subclasses must override this property to specify the section
        of the configuration they are responsible for.

        Returns:
            str: The name of the configuration section.
        """
        raise NotImplementedError()

    def read_slist(self, key: str, default: list[str]) -> list[str]:
        """
        Read a list of strings from the configuration.

        Args:
            key (str): The configuration key to read.
            default (list[str]): The default value to return if the key is not found.

        Raises:
            ConfigurationValueError: When the configuration data cannot be converted to a list of
            strings.

        Returns:
            list[str]: The list of strings from the configuration, or the default value.
        """
        return self._conf.read_slist(self.section, key, default)

    def read_ilist(self, key: str, default: list[int]) -> list[int]:
        """
        Read a list of integers from the configuration.

        Args:
            key (str): The configuration key to read.
            default (list[int]): The default value to return if the key is not found.

        Raises:
            ConfigurationValueError: When the configuration data cannot be converted to a list of
            integers.

        Returns:
            list[int]: The list of integers from the configuration, or the default value.
        """
        return self._conf.read_ilist(self.section, key, default)

    def read_str(self, key: str, default: str) -> str:
        """
        Read a string from the configuration.

        Args:
            key (str): The configuration key to read.
            default (str): The default value to return if the key is not found.

        Raises:
            ConfigurationValueError: When the configuration data cannot be converted to an str.

        Returns:
            str: The string from the configuration, or the default value.
        """
        return self._conf.read_str(self.section, key, default)

    def read_int(self, key: str, default: int) -> int:
        """
        Read an integer from the configuration.

        Args:
            key (str): The configuration key to read.
            default (int): The default value to return if the key is not found.

        Raises:
            ConfigurationValueError: When the configuration data cannot be converted to an int.

        Returns:
            int: The integer from the configuration, or the default value.
        """
        return self._conf.read_int(self.section, key, default)

    def __init__(self, host_config: IHostConfiguration) -> None:
        """
        Initialize the adapter configuration with a host configuration.

        Args:
            host_config (IHostConfiguration): The host configuration to use for reading values.
        """
        self._conf: IHostConfiguration = host_config
