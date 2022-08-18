import requests
from conftest import cmd_params


def test_url_status_code(cmd_params):
    r = requests.get(cmd_params['url'])
    assert r.status_code == cmd_params['status_code']
