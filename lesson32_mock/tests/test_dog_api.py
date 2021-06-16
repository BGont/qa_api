import pytest
from .mock_helper import mock_client


@pytest.fixture(scope="function")
def base_url_client(test_client):
    if test_client.mock_tests:
        test_client = mock_client(base_url="https://dog.ceo")
    return test_client(base_url="https://dog.ceo")


def test_breeds_list(base_url_client):
    response = base_url_client.get('/api/breeds/list/all')

    if base_url_client.mock_tests:
        response.json.return_value = {
            "status": "success"
        }

    assert response.ok, response.text
    assert response.json().get('status') == 'success'


def test_random_image(base_url_client):
    response = base_url_client.get('/api/breeds/image/random')

    if base_url_client.mock_tests:
        response.json.return_value = {
            "message": "https://images.dog.ceo/breeds/setter-gordon/n02101006_635.jpg",
            "status": "success"
        }

    assert response.ok, response.text
    assert response.json().get('status') == 'success'
    image_url = response.json().get('message')
    assert image_url.endswith('.jpg') or image_url.endswith('.jpeg')


@pytest.mark.parametrize("breed, image_count", [("setter", 3), ("basenji", 5), ("hound", 4)])
def test_multiple_random_images_by_breed(base_url_client, breed, image_count):
    path = f"/api/breed/{breed}/images/random/{image_count}"
    response = base_url_client.get(path)

    if base_url_client.mock_tests:
        response.json.return_value = {
            "message": [fr"https:\/\/images.dog.ceo\/breeds\/{breed}\/n02088094_7260.jpg"] * image_count,
            "status": "success"
        }

    assert response.ok
    assert response.json().get('status') == 'success'
    assert len(response.json().get('message')) == image_count
    for img in response.json().get('message'):
        assert img.endswith('.jpg') or img.endswith('.jpeg')


@pytest.mark.parametrize("breed, sub_breed, image_count",
                         [("hound", "blood", 3), ("sheepdog", "shetland", 5), ("terrier", "border", 4)])
def test_multiple_random_images_by_sub_breed(base_url_client, breed, sub_breed, image_count):
    path = f"/api/breed/{breed}/{sub_breed}/images/random/{image_count}"
    response = base_url_client.get(path)

    if base_url_client.mock_tests:
        response.json.return_value = {
            "message": [fr"https:\/\/images.dog.ceo\/breeds\/{breed}-{sub_breed}\/n02088094_7260.jpg"] * image_count,
            "status": "success"
        }

    assert response.ok
    assert response.json().get('status') == 'success'
    assert len(response.json().get('message')) == image_count
    for img in response.json().get('message'):
        assert img.endswith('.jpg') or img.endswith('.jpeg')


@pytest.mark.parametrize("breed, sub_breed_list", [("setter", ["english", "gordon", "irish"]), ])
def test_sub_breeds_list(base_url_client, breed, sub_breed_list):
    path = f"/api/breed/{breed}/list"
    response = base_url_client.get(path)

    if base_url_client.mock_tests:
        response.json.return_value = {
            "message": sub_breed_list,
            "status": "success"
        }

    assert response.ok, response.text
    assert response.json().get('status') == 'success'
    assert response.json().get("message") == sub_breed_list
