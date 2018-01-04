=======================
pytest fixture "xfiles"
=======================

Pytest fixtures providing data loaded from test function, test module or test package related data file (JSON, YAML, other can be added).

Motivation
==========
Some tests require complex or extended amount of data and it is cumbersome to keep the testing code and the data in the same python file.

This repository provides pytest fixtures called `xfiles`, allowing to keep the data in external files while allowing to get them loaded into relevant test very easily.

Typical format for data files is `yaml`, sometimes `json`, the solution is easy to extend for other formats.

Have `tests/test_httpbin.py` file::

    import requests


    def test_get(function_yaml):
        url = function_yaml["url"]
        resp = requests.get(url)
        assert resp.ok
        data = resp.json()
        expected = function_yaml["expected"]
        assert data["args"] == expected["args"]
        exp_headers = expected["headers"]
        data_headers = data["headers"]
        # check presence of headers
        for header_name in exp_headers["exact_value"]:
            assert header_name in data_headers
        for header_name in exp_headers["prefix_match"]:
            assert header_name in data_headers
        # check values of headers
        for header_name, exp_value in exp_headers["exact_value"].items():
            assert data_headers[header_name] == exp_value
        # check prefix
        for header_name, exp_value in exp_headers["prefix_match"].items():
            assert data_headers[header_name].startswith(exp_value)

Value of `function_yaml` is loaded (by xfile fixture) from `tests/test_httpbin.get.yaml` file::

    url: "https://httpbin.org/get"
    expected:
        args: {}
        headers:
            exact_value:
                Accept: "*/*"
                Accept-Encoding: gzip, deflate
                Connection: close 
                Host: httpbin.org 
            prefix_match:
                User-Agent: "python-requests/"

If we add another test into `tests/test_httpbin.py` file::

    def test_status(function_yaml):
        url_pattern = function_yaml["url"]
        for code, exp_reason in function_yaml["codes"].items():
            url = url_pattern.format(code=code)
            resp = requests.get(url)
            assert resp.status_code == code
            assert resp.reason == exp_reason

and related `tests/test_httpbin.status.yaml`::

    url: https://httpbin.org/status/{code}
    codes:
        200: OK
        201: CREATED
        202: ACCEPTED
        203: NON AUTHORITATIVE INFORMATION
        204: NO CONTENT
        205: RESET CONTENT
        206: PARTIAL CONTENT
        207: MULTI STATUS
        226: IM USED

one may wonder, how it comes, that even though both tests use the same fixture `function_yaml`, the data provided by this fixture clearly differs for each test. The trick is, that each time, the file name to load data from is derived using the test function name being called.

Fixtures provided
=================
`{scope}_xfile` family
----------------------
Having `tests/sub/test_thing.py` with a test function `test_fun`, following fixtures would return path to an X-files as follows:

- `function_xfile`: `tests/sub/test_thing.test_fun._x_`
- `module_xfile`: `tests/sub/test_thing._x_`
- `package_xfile`: `tests/sub/__init__._x_`

Each fixture provides path to a file with base name derived from current function, module or package and with an extension `"._x_"`.


This fixture is not usually used directly, but is used to derive another fixture loading data from a file with specific extension.

An example of derived fixture can be existing fixture `function_json`::

    @pytest.fixture(scope="function")
    def function_json(function_xfile):
        path = function_xfile.with_suffix(".json")
        with path.open(encoding="utf-8") as f:
            import json
            return json.load(f)

The fixture takes advantage of the filename calculated for given function, replaces extension with
`.json`, loads the data from such a file and returns it.

`{scope}_json` family
---------------------
Having `tests/sub/test_thing.py` with a test function `test_fun`, following fixtures would return data loaded from JSON files as follows:

- `function_json`: `tests/sub/test_thing.test_fun.json`
- `module_json`: `tests/sub/test_thing.json`
- `package_json`: `tests/sub/__init__.json`


`{scope}_yaml` family
---------------------
Having `tests/sub/test_thing.py` with a test function `test_fun`, following fixtures would return data loaded from YAML files as follows:

- `function_yaml`: `tests/sub/test_thing.test_fun.yaml`
- `module_yaml`: `tests/sub/test_thing.yaml`
- `package_yaml`: `tests/sub/__init__.yaml`
