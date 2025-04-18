"""
tests.mocks Module

This module contains mock class for use as dependencies for the unit-under-test. Each mock class
should end with the word "Mock" and be exposed in the __all__ list of this module.
"""


from .config_set_repo_mock import ConfigSetRepositoryMock


__all__ = [
    "ConfigSetRepositoryMock"
]

