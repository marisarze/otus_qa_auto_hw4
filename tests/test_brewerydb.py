import requests
import pytest
import cerberus
import random
from utility import base_validation


DATE_TIME_REGEX = "^[0-9]{4}-(((0[13578]|(10|12))-(0[1-9]|[1-2][0-9]|3[0-1]))|(02-(0[1-9]|[1-2][0-9]))|((0[469]|11)-(0[1-9]|[1-2][0-9]|30)))T(?:1[0-2]|0?[1-9]):[0-5]\d:[0-5]\d\.[0-9]{3}[A-Z]{1}"
PHONE_NUM_REGEX = "[0-9]{0,11}|([0-9]{0,4}-[0-9]{0,4}-[0-9]{0,4})"

BREWERY_INFO_SCHEMA = {
    "id": {'type': 'string'},
    "name":{'type': 'string'},
    "brewery_type":{'type': 'string', 'allowed': ['micro', 'nano', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract', 'proprietor', 'closed'], 'nullable': True},
    "street":{'type': 'string', 'nullable': True},
    "address_2":{'type': 'string', 'nullable': True},
    "address_3":{'type': 'string', 'nullable': True},
    "city":{'type': 'string', 'nullable': True},
    "state":{'type': 'string', 'nullable': True},
    "county_province":{'type': 'string', 'nullable': True},
    "postal_code":{'type': 'string', 'nullable': True},
    "country":{'type': 'string', 'nullable': True},
    "longitude":{'type': 'string', 'nullable': True},
    "latitude":{'type': 'string', 'nullable': True},
    "phone":{'type': 'string', 'regex': PHONE_NUM_REGEX, 'nullable': True},
    "website_url":{'type': 'string', 'nullable': True},
    "updated_at":{'type': 'string', 'regex': DATE_TIME_REGEX, 'nullable': True},
    "created_at":{'type': 'string', 'regex': DATE_TIME_REGEX, 'nullable': True}
}


def test_single_brewery():
    url = "https://api.openbrewerydb.org/breweries/banjo-brewing-fayetteville"
    info = base_validation(url)
    v = cerberus.Validator(BREWERY_INFO_SCHEMA)
    assert v.validate(info)


cities = ["dallas", "petersburg", "moscow", "texas"]
@pytest.mark.parametrize('city', cities)
def test_get_by_city(city):
    url = f"https://api.openbrewerydb.org/breweries?by_city={city}&per_page=10"
    info = base_validation(url)
    v = cerberus.Validator(BREWERY_INFO_SCHEMA)
    for brewery in info:
        assert v.validate(brewery)
        assert brewery['city'].lower().__contains__(city)


brewery_types = ['micro', 'nano', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract', 'proprieter', 'closed']
@pytest.mark.parametrize('brewery_type', brewery_types)
def test_get_by_brewery_type(brewery_type):
    url = f"https://api.openbrewerydb.org/breweries?by_type={brewery_type}&per_page=10"
    info = base_validation(url)
    v = cerberus.Validator(BREWERY_INFO_SCHEMA)
    for brewery in info:
        assert v.validate(brewery)
        assert brewery['brewery_type'] == brewery_type


content_length = [0, 1, 2, 5, 10]
@pytest.mark.parametrize('content_length', content_length)
def test_change_page_length(content_length):
    page_number = random.randint(0,10)
    url = f"https://api.openbrewerydb.org/breweries?page={page_number}&per_page={content_length}"
    info = base_validation(url)
    assert len(info)==content_length
    v = cerberus.Validator(BREWERY_INFO_SCHEMA)
    for brewery in info:
        assert v.validate(brewery)


def test_get_sorted_by_phone():
    url = "https://api.openbrewerydb.org/breweries?by_state=ohio&sort=phone,name:asc&per_page=50"
    info = base_validation(url)
    assert len(info)==50
    v = cerberus.Validator(BREWERY_INFO_SCHEMA)
    for brewery in info:
        assert v.validate(brewery)
        assert brewery['state']=='Ohio'