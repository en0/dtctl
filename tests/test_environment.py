import pytest


def test_environment_can_run_unittests_correctly():
    assert True


def test_environment_can_access_dflib():
    import sys

    print("PYTHONPATH: ", sys.path)
    try:
        import dflib
        dflib.__file__
    except ImportError:
        pytest.fail("Unable to import dflib")
    except AttributeError:
        pytest.fail("Imported module 'dflib' is not accessable.")


def test_environment_can_access_dfctl():
    try:
        import dfctl
        dfctl.__file__
    except ImportError:
        pytest.fail("Unable to import dfctl")
    except AttributeError:
        pytest.fail("Imported module 'dfctl' is not accessable.")


def test_environment_can_access_fixtures():
    try:
        from tests import fixtures
        fixtures.__file__
    except ImportError:
        pytest.fail("Unable to import tests.fixtures")
    except AttributeError:
        pytest.fail("Imported module 'tests.fixtures' is not accessable.")


def test_environment_can_access_helpers():
    try:
        from tests import helpers
        helpers.__file__
    except ImportError:
        pytest.fail("Unable to import tests.helpers")
    except AttributeError:
        pytest.fail("Imported module 'tests.helpers' is not accessable.")
