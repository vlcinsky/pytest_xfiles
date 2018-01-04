import pytest


def test_happy(function_yaml):
    print("function_yaml in test #1", function_yaml)


def test_list(function_yaml):
    print("function_yaml in test #2", function_yaml)


def test_indir(blob):
    print("blob-indir", blob)


def test_module_yaml(module_yaml):
    print("module:", module_yaml)


def test_package_yaml(package_yaml, function_yaml):
    print("module:", package_yaml)
    print("function:", function_yaml)
