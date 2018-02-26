=======================
pytest fixture "xfiles"
=======================

Each test function deserves a companion - a small or large (YAML, JSON or other) file sitting beside.

Providing such data can be as simple as:

.. code-block:: python

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

Run the test:

.. code-block:: bash

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

Where are the files?

.. code-block:: bash

    $ ls tests/shakespeare/test_romeoyjulieta.*
    tests/shakespeare/test_romeoyjulieta.julieta.yaml
    tests/shakespeare/test_romeoyjulieta.py
    tests/shakespeare/test_romeoyjulieta.romeo.yaml
    tests/shakespeare/test_romeoyjulieta.yaml

and one more (for the whole package `tests.shakespeare`):

.. code-block:: bash

    $ ls tests/shakespeare/__init__.yaml
    tests/shakespeare/__init__.yaml

File formats supported
======================
The sample above shows use of YAML formatted data. Out of the box, JSON format is also supported via `function_json`, `module_json` and `package_json` fixtures.

More formats can be supported (see below).

The `function`, the `module` and the `package`
==============================================

The file `tests/shakespeare/__init__.py` defines a test **package**.

The file `tests/shakespeare/test_romeoyjulieta` is a test **module**

The `def test_romeo` as in:

.. code-block:: python

   def test_romeo(function_yaml):
       print(function_yaml)

defines a test **function**.

Currently there is no notion of test **class** as I did not need it. It may appear later on.

Names of data files
===================
Data file names are derived from related object (package, module, function) and use format specific extensions (`.json`, `.yaml`, special `._x_`, other can be added).

Package data file has name `__init__.py` with extension changed to format specific one, e.g. `__init__.json`.

Module data file has name such as `test_romeoyjulieta.py` with extension changed to format specific one, e.g. `test_romeoyjulieta.json`.

In case of test function, test function name must be added. To make files more readable, the `test_` part of the function is removed. For `test_romeo` function can be e.g. `test_romeoyjulieta.romeo.json`.

The files are typically in the same directory as relevant python test suite code.

What are the `._x_` files?
==========================
There are special fixtures `function_xfile`, `module_xfile` and `package_xfile`, which only return path to a file with extension `._x_` (and do not attempt to load the content).

The `._x_` files are used as base for implementing other fixtures, e.g. as for JSON:

.. code-block:: python

    @pytest.fixture(scope="function")
    def function_json(function_xfile):
        path = function_xfile.with_suffix(".json")
        with path.open(encoding="utf-8") as f:
            import json
            return json.load(f)

As shown, the `function_json` simply takes the `._x_` file path, replaces the extension with it's own `.json` and returns data loaded from such file.

Adding support for other data formats (e.g. CSV)
================================================
Following the `function_json` example above, we may load data from any other data file, e.g. for `.csv`:

.. code-block:: python

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
It is easy to take any of data availalbe and use it to create object of your preference. E.g. assuming that the `package_yaml` returns information about author in form of dictionary with keys "name" and "surname", one can create fixture `classy_author` returning specific class instance. Put following into `conftest.py`:

.. code-block:: python

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

and use it from test `test_classy_author.py`:

.. code-block:: python

    def test_custom_fixture(classy_author):
        print(classy_author.full_name)


Fixtures provided
=================
Here is summary of fixtures provided. In all cases we assume we have `tests/sub/test_thing.py` with a test function `test_fun` and all required data files are available.

`{scope}_xfile` family
----------------------
Each fixture provides path to a file with base name derived from current function, module or package and with an extension `"._x_"`:

- `function_xfile`: `tests/sub/test_thing.test_fun._x_`
- `module_xfile`: `tests/sub/test_thing._x_`
- `package_xfile`: `tests/sub/__init__._x_`


`{scope}_json` family
---------------------
Fixtures provide data loaded from the JSON formatted files:

- `function_json`: `tests/sub/test_thing.test_fun.json`
- `module_json`: `tests/sub/test_thing.json`
- `package_json`: `tests/sub/__init__.json`


`{scope}_yaml` family
---------------------
Fixtures provide data loaded from the YAML formatted files:

- `function_yaml`: `tests/sub/test_thing.test_fun.yaml`
- `module_yaml`: `tests/sub/test_thing.yaml`
- `package_yaml`: `tests/sub/__init__.yaml`

Note on YAML package and YAML version
=====================================
Switched from `pyyaml` to `ruamel.yaml` as it supports YAML version 1.2.

If you require YAML files using version 1.1, use `% YAML 1.1` in your YAML file.
