=======================
pytest fixture "xfiles"
=======================

Each test function deserves a companion - a small or large (YAML, JSON or other) file siting beside.

Providing such data can be as simple as::

    """Test Romeo y Julieta by Shakespeare.
    """


    def test_romeo(function_yaml):
        print(function_yaml)


    def test_julieta(function_yaml):
        print(function_yaml)


    def test_play(module_yaml):
        print(module_yaml)


    def test_author(package_yaml):
        print(package_yaml)

Run the test::

    $ pytest -sv tests/shakespeare/test_romeoyjulieta.py
    ============================= test session starts ==============================
    ...

    tests/shakespeare/test_romeoyjulieta.py::test_romeo {'name': 'Romeo', 'mindmap': ['Julieta', 'Julieta', 'Julieta'], 'spot': 'ladder'}
    PASSED
    tests/shakespeare/test_romeoyjulieta.py::test_julieta {'name': 'Julieta', 'mindmap': ['Romeo', 'Romeo', 'Romeo'], 'spot': 'balcony'}
    PASSED
    tests/shakespeare/test_romeoyjulieta.py::test_play {'story': 'Romeo y Julieta', 'main_characters': ['Romeo', 'Julieta'], 'location': 'Verona'}
    PASSED
    tests/shakespeare/test_romeoyjulieta.py::test_author {'name': 'William', 'surname': 'Shakespeare'}
    PASSED

    =========================== 4 passed in 0.03 seconds ===========================

Where are the files?::

    $ ls tests/shakespeare/test_romeoyjulieta.*
    tests/shakespeare/test_romeoyjulieta.julieta.yaml
    tests/shakespeare/test_romeoyjulieta.py
    tests/shakespeare/test_romeoyjulieta.romeo.yaml
    tests/shakespeare/test_romeoyjulieta.yaml

and one more (for the whole package `tests.shakespeare`)::

    $ ls tests/shakespeare/__init__.yaml
    tests/shakespeare/__init__.yaml

File formats supported
======================
The sample above shows use of YAML formatted data. Out of the box, JSON format is also supported via `function_json`, `module_json` and `package_json` fixtures.

More formats can be supported (see later).

The `function`, the `module` and the `package`
==============================================

The file `tests/shakespeare/__init__.py` defines a test *package*.

The file `tests/shakespeare/test_romeoyjulieta` is a test *module*

The `def test_romeo` as in::

    def test_romeo(function_yaml):
        print(function_yaml)

defines a test *function*.

Currently there is no notion of test *class* as I did not need it. It may appear later on.

Names of data files
===================
Data file names are derived from related object (package, module, function) and use format specific extentions (`.json`, `.yaml`, special `._x_`, other can be added).

Package data file has name `__init__.py` with extension changed to format specific one, e.g. `__init__.json`.

Module data file has name such as `test_romeoyjulieta.py` with extension changed to format specific one, e.g. `test_romeoyjulieta.json`.

In case of test function, test function name must be added. To make files more readable, the `test_` part of the function is removed. For `test_romeo` function can be e.g. `test_romeoyjulieta.romeo.json`.

The files are typically in the same directory as relevant python test suite code.

What are the `._x_` files?
==========================
There are special fixtures `function_xfile`, `module_xfile` and `package_xfile`, which only return path to a file with extension `._x_` (and do not attempt to load the content).

The `._x_` files are used as base for implementing other fixtures, e.g. as for JSON::

    @pytest.fixture(scope="function")
    def function_json(function_xfile):
        path = function_xfile.with_suffix(".json")
        with path.open(encoding="utf-8") as f:
            import json
            return json.load(f)

As shown, the `function_json` simply takes the `._x_` file path, replaces the extension with it's own `.json` and return data loaded from such file.

Adding support for other data formats (e.g. CSV)
================================================
Following the `function_json` example above, we may load data from any other data file, e.g. for `.csv`::

    from csv import reader

    import pytest


    @pytest.fixture(scope="function")
    def function_csv(function_xfile):
        path = function_xfile.with_suffix(".csv")
        with path.open(encoding="utf-8") as f:
            return list(reader(f))


    def test_codes(function_csv):
        print(function_csv)

.. warning::

    Unlike the `{function,module,package}_json` and `{function,module,package}_yaml` fixtures, the `function_csv` (and all the variants) fixture is not provided by this pytest plugin.

    Such fixture is intentionally not implemented as it shall be easy to implement it using your prefered extension, delimiter, encoding, type of returned object (data, iterator...) etc.

Creating fixtures based on provided data
========================================
It is easy to take any of data availalbe and use it to create object of your preference. E.g. assuming that the `package_yaml` returns information about author in form of dictionary with keas "name" and "surname", one can create fixture `classy_author` returning specific class instance. Put following into `conftest.py`::

    @pytest.fixture(scope="module")
    def classy_author(package_yaml):
        return Author(package_yaml["name"], package_yaml["surname"])

and use it from test `test_classy_author.py`::

    def test_custom_fixture(classy_author):
        print(classy_author.full_name)


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
