"""Test loading data from CSV file.
"""
from csv import reader

import pytest


@pytest.fixture(scope="function")
def function_csv(function_xfile):
    path = function_xfile.with_suffix(".csv")
    with path.open(encoding="utf-8") as f:
        return list(reader(f))


def test_codes(function_csv):
    print(function_csv)
