from copy import copy
from random import randint
import pytest

from .mock_helper import mock_client

SAMPLE_BREWERY = {
    "id": 9094,
    "obdb_id": "bnaf-llc-austin",
    "name": "Bnaf, LLC",
    "brewery_type": "planning",
    "street": "null",
    "address_2": "null",
    "address_3": "null",
    "city": "Austin",
    "state": "Texas",
    "county_province": "null",
    "postal_code": "78727-7602",
    "country": "United States",
    "longitude": "null",
    "latitude": "null",
    "phone": "null",
    "website_url": "null",
    "updated_at": "2018-07-24T00:00:00.000Z",
    "created_at": "2018-07-24T00:00:00.000Z"
}


@pytest.fixture(scope="module")
def base_url_client(test_client):
    if test_client.mock_tests:
        test_client = mock_client(base_url="https://api.openbrewerydb.org")
    return test_client(base_url="https://api.openbrewerydb.org")


def test_breeds_list(base_url_client):
    response = base_url_client.get('/breweries')
    assert response.ok, response.text


@pytest.mark.parametrize("cities",
                         [("Austin", "Austintown", "Port Austin"), ("Jackson", "Jacksonville", "Jacksonville Beach")])
def test_get_breweries_by_city(base_url_client, cities):
    random_city = cities[randint(0, len(cities)-1)]
    response = base_url_client.get("/breweries", params={"by_city": random_city.lower()})

    if base_url_client.mock_tests:
        brewery = copy(SAMPLE_BREWERY)
        brewery["city"] = random_city
        response.json.return_value = [brewery] * 10

    assert response.ok, response.text
    response_data = response.json()
    for item in response_data:
        assert item["city"] in cities


@pytest.mark.parametrize("brewery_type", ["micro", "nano", "regional"])
def test_get_breweries_by_type(base_url_client, brewery_type):
    response = base_url_client.get("/breweries", params={"by_type": brewery_type})

    if base_url_client.mock_tests:
        brewery = copy(SAMPLE_BREWERY)
        brewery["brewery_type"] = brewery_type
        response.json.return_value = [brewery] * 10

    assert response.ok, response.text
    response_data = response.json()
    for item in response_data:
        assert item["brewery_type"] == brewery_type


@pytest.mark.parametrize("brewery_id", [11767, 11609, 12448])
def test_get_brewery(base_url_client, brewery_id):
    path = f"/breweries/{brewery_id}"
    response = base_url_client.get(path)

    if base_url_client.mock_tests:
        brewery = copy(SAMPLE_BREWERY)
        brewery["id"] = brewery_id
        response.json.return_value = brewery

    assert response.ok, response.text
    assert response.json()['id'] == brewery_id


@pytest.mark.parametrize("term", ["Kid", "beer", "home"])
def test_autocomplete_brewery(base_url_client, term):
    response = base_url_client.get("/breweries/autocomplete", params={"query": term.lower()})

    if base_url_client.mock_tests:
        brewery = {
            "id": SAMPLE_BREWERY["id"],
            "name": SAMPLE_BREWERY["name"]
        }
        response.json.return_value = [brewery] * 10

    assert response.ok, response.text
    response_data = response.json()
    for item in response_data:
        assert list(item.keys()) == ["id", "name"]
    assert len(response_data) <= 15
