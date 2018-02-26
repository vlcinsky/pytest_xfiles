"""pytest fixtures x-files
"""
from pathlib import Path
import pytest


@pytest.fixture(scope="function")
def function_xfile(request):
    func_name = request.function.__name__
    test_name = func_name.split("_", 1)[-1]
    module_path = request.module.__file__
    return Path(module_path).with_suffix(
        ".{test_name}._x_".format(test_name=test_name))


@pytest.fixture(scope="module")
def module_xfile(request):
    module_path = Path(request.module.__file__)
    return module_path.with_suffix("._x_")


@pytest.fixture(scope="module")
def package_xfile(request):
    module_path = Path(request.module.__file__)
    return module_path.with_name("__init__._x_")


@pytest.fixture(scope="function")
def function_yaml(function_xfile):
    path = function_xfile.with_suffix(".yaml")
    with path.open(encoding="utf-8") as f:
        from ruamel.yaml import YAML
        yaml = YAML()
        return yaml.load(f)


@pytest.fixture(scope="module")
def module_yaml(module_xfile):
    path = module_xfile.with_suffix(".yaml")
    with path.open(encoding="utf-8") as f:
        from ruamel.yaml import YAML
        yaml = YAML()
        return yaml.load(f)


@pytest.fixture(scope="module")
def package_yaml(package_xfile):
    path = package_xfile.with_suffix(".yaml")
    with path.open(encoding="utf-8") as f:
        from ruamel.yaml import YAML
        yaml = YAML()
        return yaml.load(f)


@pytest.fixture(scope="function")
def function_json(function_xfile):
    path = function_xfile.with_suffix(".json")
    with path.open(encoding="utf-8") as f:
        import json
        return json.load(f)


@pytest.fixture(scope="module")
def module_json(module_xfile):
    path = module_xfile.with_suffix(".json")
    with path.open(encoding="utf-8") as f:
        import json
        return json.load(f)


@pytest.fixture(scope="module")
def package_json(package_xfile):
    path = package_xfile.with_suffix(".json")
    with path.open(encoding="utf-8") as f:
        import json
        return json.load(f)
