import requests
import re
import json
import pytest


IMAGE_CONTENT_TYPES = ['image/g3fax', 'image/gif', 'image/ief', 'image/jpeg', 'image/tiff', 'image/png']

def test_random_breed():
    url = "https://dog.ceo/api/breeds/image/random"
    regexp = "^https:\/\/images\.dog\.ceo\/breeds\/([a-zA-Z0-9]*){1}(-[a-zA-Z0-9]*)?\/([a-zA-Z0-9_ -]+){1}\.[a-zA-Z0-9]+"
    with open("tests/breeds.json", 'r') as file:
        breeds = json.load(file)
    for i in range(10):
        r = requests.get(url)
        assert r.status_code == 200
        assert r.headers['content-type'] == 'application/json'
        assert r.encoding == 'utf-8'

        info = r.json()
        assert info['status'] == "success"
        result = re.search(regexp, info['message']) 
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


# @pytest.mark.parametrize('breed', breed_generator())
# def test_breed_requests(breed):
#     url = f"https://dog.ceo/api/breed/{breed}/images"
#     r = requests.get(url)
#     assert r.status_code == 200
#     assert r.headers['content-type'] == 'application/json'
#     assert r.encoding == 'utf-8'
#     info = r.json()
#     assert info['status'] == "success"
#     assert isinstance(info["message"], list)
#     for img_url in info["message"]:
#         img_response = requests.get(img_url)
#         assert img_response.status_code == 200
#         assert img_response.headers['content-type'] in IMAGE_CONTENT_TYPES



@pytest.mark.parametrize('breed', breed_generator())
def test_random_image_by_breed(breed):
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'application/json'
    assert r.encoding == 'utf-8'
    info = r.json()
    assert info['status'] == "success"
    img_response = requests.get(info['message'])
    assert img_response.status_code == 200
    assert img_response.headers['content-type'] in IMAGE_CONTENT_TYPES


def breed_info_generator():
    with open("tests/breeds.json", 'r') as file:
        breeds = json.load(file)
    for breed in breeds.keys():
        yield breed, breeds[breed]


@pytest.mark.parametrize('breed', 'subbreeds', breed_generator())
def test_get_subbreed_list(breeds, subbreeds):
    url = f"https://dog.ceo/api/breed/{breed}/list"
    regexp = "^https:\/\/images\.dog\.ceo\/breeds\/([a-zA-Z0-9]*){1}(-[a-zA-Z0-9]*)?\/([a-zA-Z0-9_ -]+){1}\.[a-zA-Z0-9]+"
    with open("tests/breeds.json", 'r') as file:
        breeds = json.load(file)
    for i in range(10):
        r = requests.get(url)
        assert r.status_code == 200
        assert r.headers['content-type'] == 'application/json'
        assert r.encoding == 'utf-8'

        info = r.json()
        assert info['status'] == "success"
        result = re.search(regexp, info['message']) 
        breed = result.group(1)
        
        assert breed in breeds.keys()
        if len(breeds[breed])!=0:
            subbreed = result.group(2)[1:]
            assert subbreed in breeds[breed]
        img_response = requests.get(info['message'])
        assert img_response.status_code == 200
        assert img_response.headers['content-type'] in IMAGE_CONTENT_TYPES
#test_breed_requests(breeds)
#test_random_breed()