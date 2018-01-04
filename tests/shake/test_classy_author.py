"""Test user defined fixture `classy_author` (see `conftest.py`) derived from
`package_yaml`. """


def test_custom_fixture(classy_author):
    print(classy_author.full_name)
