import requests
import pytest


def base_validation(url, content_types=['application/json', 'application/json; charset=utf-8']):
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'] in content_types
    assert r.encoding == 'utf-8'
    return r.json()