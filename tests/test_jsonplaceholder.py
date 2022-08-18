import pytest
import cerberus
import requests
import cloudscraper
from utility import base_validation

@pytest.mark.parametrize('post_id', [i for i in range(10)])
def test_get_comments_by_post(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    info = base_validation(url)
    schema = {
        "postId": {'type': 'integer'},
        "id": {'type': 'integer'},
        "name": {'type': 'string'},
        "email": {'type': 'string'},
        "body": {'type': 'string'}
    }
    for entry in info:
        v = cerberus.Validator(schema)
        assert entry['postId'] == post_id


@pytest.mark.parametrize('album_id', [i for i in range(10)])
def test_get_photo_by_album(album_id):
    session = requests.Session()
    headers = {'Content-type': 'application/json; charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f"https://jsonplaceholder.typicode.com/albums/{album_id}/photos"
    r = session.get(url, headers=headers)
    assert r.status_code == 200
    assert r.headers['content-type'] in ['application/json', 'application/json; charset=utf-8']
    assert r.encoding == 'utf-8'
    info = r.json()
    schema = {
        "albumId": {'type': 'integer'},
        "id": {'type': 'integer'},
        "title": {'type': 'string'},
        "url": {'type': 'string'},
        "thumbnailUrl": {'type': 'string'}
    }
    for entry in info:
        v = cerberus.Validator(schema)
        assert entry['albumId'] == album_id
        r = session.get(entry['url'], headers=headers)
        assert r.status_code == 200
        r = session.get(entry['thumbnailUrl'], headers=headers)
        assert r.status_code == 200


@pytest.mark.parametrize('user_id', [i for i in range(10)])
def test_get_album_by_user(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}/albums"
    info = base_validation(url)
    schema = {
        "userId": {'type': 'integer'},
        "id": {'type': 'integer'},
        "title": {'type': 'string'}
    }
    for entry in info:
        v = cerberus.Validator(schema)
        assert entry['userId'] == user_id


@pytest.mark.parametrize('user_id', [i for i in range(10)])
def test_get_todos_by_user(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}/albums"
    info = base_validation(url)
    schema = {
        "userId": {'type': 'integer'},
        "id": {'type': 'integer'},
        "title": {'type': 'string'},
        "completed": {'type': 'boolean'}
    }
    for entry in info:
        v = cerberus.Validator(schema)
        assert entry['userId'] == user_id


@pytest.mark.parametrize('user_id', [i for i in range(10)])
def test_get_posts_by_user(user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}/posts"
    info = base_validation(url)
    schema = {
        "userId": {'type': 'integer'},
        "id": {'type': 'integer'},
        "title": {'type': 'string'},
        "body": {'type': 'string'}
    }
    for entry in info:
        v = cerberus.Validator(schema)
        assert entry['userId'] == user_id
