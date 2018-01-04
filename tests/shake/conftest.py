import pytest


@pytest.fixture(scope="function")
def character(function_yaml):
    return function_yaml


@pytest.fixture(scope="module")
def play(module_yaml):
    return module_yaml


@pytest.fixture(scope="module")
def author(package_yaml):
    return package_yaml


class Author(object):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    @property
    def full_name(self):
        return "{self.name} {self.surname}".format(self=self)


@pytest.fixture(scope="module")
def classy_author(package_yaml):
    return Author(package_yaml["name"], package_yaml["surname"])
