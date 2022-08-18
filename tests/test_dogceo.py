import requests
import re
import json
import pytest
import cerberus
from utility import base_validation

IMAGE_CONTENT_TYPES = ['image/g3fax', 'image/gif', 'image/ief', 'image/jpeg', 'image/tiff', 'image/png']
IMAGE_URL_REGEXP = "^https:\/\/images\.dog\.ceo\/breeds\/([a-zA-Z0-9]*){1}(-[a-zA-Z0-9]*)?\/([^\>]*){1}\.[a-zA-Z0-9]+"


def test_breed_list():
    url = "https://dog.ceo/api/breeds/list/all"
    info = base_validation(url)
    schema = {
    'status': {'type': 'string', 'allowed': ['success']},
    'message': {'type': 'dict', 
            'keysrules': {'type': 'string'},
            'valuesrules': {'type': 'list', 'schema': {'type': 'string'}}}
    }
    v = cerberus.Validator(schema)
    assert v.validate(info)
    with open("tests/breeds.json", 'r') as file:
        breeds = json.load(file)
    for key in info['message'].keys():
        assert info['message'][key] == breeds[key]


def test_random_breed():
    url = "https://dog.ceo/api/breeds/image/random"
    with open("tests/breeds.json", 'r') as file:
        breeds = json.load(file)
    for i in range(10):
        info = base_validation(url)

        schema = {
        'status': {'type': 'string', 'allowed': ['success']},
        'message': {'type': 'string', 'regex': IMAGE_URL_REGEXP}
        }
        v = cerberus.Validator(schema)
        assert v.validate(info)

        result = re.search(IMAGE_URL_REGEXP, info['message']) 
        breed = result.group(1)
        
        assert breed in breeds.keys()
        if len(breeds[breed])!=0:
            subbreed = result.group(2)[1:]
            assert subbreed in breeds[breed]
        img_response = requests.get(info['message'])
        assert img_response.status_code == 200
        assert img_response.headers['content-type'] in IMAGE_CONTENT_TYPES


def breed_generator():
    with open("tests/breeds.json", 'r') as file:
        breeds = json.load(file)
    for breed in breeds.keys():
        yield breed


@pytest.mark.parametrize('breed', breed_generator())
def test_breed_requests(breed):
    url = f"https://dog.ceo/api/breed/{breed}/images"
    info = base_validation(url)
    
    schema = {
    'status': {'type': 'string', 'allowed': ['success']},
    'message': {'type': 'list', 'schema': {'type': 'string', 'regex': IMAGE_URL_REGEXP}}
    }
    v = cerberus.Validator(schema)
    assert v.validate(info)

    for i, img_url in enumerate(info["message"]):
        if i==2: break
        img_response = requests.get(img_url)
        assert img_response.status_code == 200
        assert img_response.headers['content-type'] in IMAGE_CONTENT_TYPES


@pytest.mark.parametrize('breed', breed_generator())
def test_random_image_by_breed(breed):
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    info = base_validation(url)
    assert info['status'] == "success"
    img_response = requests.get(info['message'])
    assert img_response.status_code == 200
    assert img_response.headers['content-type'] in IMAGE_CONTENT_TYPES


def breed_subbreeds_generator():
    with open("tests/breeds.json", 'r') as file:
        breeds = json.load(file)
    for breed in breeds.keys():
        yield (breed, breeds[breed])


@pytest.mark.parametrize('breed, subbreeds', breed_subbreeds_generator())
def test_get_subbreed_list(breed, subbreeds):
    url = f"https://dog.ceo/api/breed/{breed}/list"
    info = base_validation(url)
    assert info['status'] == "success"
    assert info['message'] == subbreeds

