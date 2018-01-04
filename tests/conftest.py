import pytest


@pytest.fixture
def blob(module_yaml):
    return "BLOB>>{module_yaml}<<BLOB".format(module_yaml=module_yaml)
