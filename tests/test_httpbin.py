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


def test_status(function_yaml):
    url_pattern = function_yaml["url"]
    for code, exp_reason in function_yaml["codes"].items():
        url = url_pattern.format(code=code)
        resp = requests.get(url)
        assert resp.status_code == code
        assert resp.reason == exp_reason
