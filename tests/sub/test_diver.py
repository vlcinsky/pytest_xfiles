"""Doc test is good.
"""


def test_happy(function_yaml):
    print(" in test #1", function_yaml)


def test_list(function_yaml, module_yaml):
    print("scenario in test #2:fun:", function_yaml)
    print("scenario in test #2:module:", module_yaml)
