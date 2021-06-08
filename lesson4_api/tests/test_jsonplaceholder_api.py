import pytest


@pytest.fixture(scope="module")
def base_url_client(test_client):
    return test_client(base_url="https://jsonplaceholder.typicode.com")


def test_get_all_posts(base_url_client):
    response = base_url_client.get('/posts')
    assert response.ok, response.text
    assert len(response.json()) == 100


@pytest.mark.parametrize("post_id", [2, 46, 54])
def test_get_post_by_id(base_url_client, post_id):
    post_fields = ["userId", "id", "title", "body"]
    path = f"/posts/{post_id}"
    response = base_url_client.get(path)
    assert response.ok, response.text
    post = response.json()
    assert list(post.keys()) == post_fields
    assert post["id"] == post_id


@pytest.mark.parametrize("post_id", [7, 88, 99])
def test_get_comments_by_post(base_url_client, post_id):
    path = f"/posts/{post_id}/comments"
    response = base_url_client.get(path)
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
    assert response.ok, response.text
    response_data = response.json()
    assert response_data[post_field] == new_value
