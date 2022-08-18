import pytest


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://ya.ru", help ="url for check status_code")
    parser.addoption("--status_code", action="store", default="200", help="expected status code for url")


@pytest.fixture
def cmd_params(request):
    config_param = {}
    config_param["url"] = request.config.getoption("--url")
    config_param["status_code"] = int(request.config.getoption("--status_code"))
    return config_param