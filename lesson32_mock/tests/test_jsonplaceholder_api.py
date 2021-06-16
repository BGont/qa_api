from copy import copy
import pytest

from .mock_helper import mock_client

SAMPLE_POST = {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas "}

SAMPLE_COMMENT = {
    "postId": 7,
    "id": 31,
    "name": "ex velit ut cum eius odio ad placeat",
    "email": "Buford@shaylee.biz",
    "body": "quia incidunt ut\naliquid est ut rerum deleniti iure est\nipsum quia ea sint et\nvoluptatem "
}


@pytest.fixture(scope="module")
def base_url_client(test_client):
    if test_client.mock_tests:
        test_client = mock_client(base_url="https://jsonplaceholder.typicode.com")
    return test_client(base_url="https://jsonplaceholder.typicode.com")


def test_get_all_posts(base_url_client):
    response = base_url_client.get('/posts')

    if base_url_client.mock_tests:
        response.json.return_value = [SAMPLE_POST] * 100

    assert response.ok, response.text
    assert len(response.json()) == 100


@pytest.mark.parametrize("post_id", [2, 46, 54])
def test_get_post_by_id(base_url_client, post_id):
    post_fields = ["userId", "id", "title", "body"]
    path = f"/posts/{post_id}"
    response = base_url_client.get(path)

    if base_url_client.mock_tests:
        post = copy(SAMPLE_POST)
        post["id"] = post_id
        response.json.return_value = post

    assert response.ok, response.text
    post = response.json()
    assert list(post.keys()) == post_fields
    assert post["id"] == post_id


@pytest.mark.parametrize("post_id", [7, 88, 99])
def test_get_comments_by_post(base_url_client, post_id):
    path = f"/posts/{post_id}/comments"
    response = base_url_client.get(path)

    if base_url_client.mock_tests:
        comment = copy(SAMPLE_COMMENT)
        comment["postId"] = post_id
        response.json.return_value = [comment] * 10

    assert response.ok, response.text
    response_data = response.json()
    for comment in response_data:
        assert comment["postId"] == post_id


@pytest.mark.parametrize("post_id", [3, 55, 77])
def test_delete_post(base_url_client, post_id):
    path = f"/posts/{post_id}"
    response = base_url_client.delete(path)
    assert response.ok, response.text


@pytest.mark.parametrize("post_id, post_field, new_value", [(4, "title", "New_title_4"), (12, "body", "New_body_12")])
def test_edit_post_field(base_url_client, post_id, post_field, new_value):
    path = f"/posts/{post_id}"
    response = base_url_client.patch(path, data={post_field: new_value})

    if base_url_client.mock_tests:
        post = copy(SAMPLE_POST)
        post["id"] = post_id
        post[post_field] = new_value
        response.json.return_value = post

    assert response.ok, response.text
    response_data = response.json()
    assert response_data[post_field] == new_value
