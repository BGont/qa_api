import pytest
from random import randint


@pytest.fixture(scope="module")
def base_url_client(test_client):
    return test_client(base_url="https://api.openbrewerydb.org")


def test_breeds_list(base_url_client):
    response = base_url_client.get('/breweries')
    assert response.ok, response.text


@pytest.mark.parametrize("cities",
                         [("Austin", "Austintown", "Port Austin"), ("Jackson", "Jacksonville", "Jacksonville Beach")])
def test_get_breweries_by_city(base_url_client, cities):
    random_city = cities[randint(0, len(cities)-1)]
    response = base_url_client.get("/breweries", params={"by_city": random_city.lower()})
    assert response.ok, response.text
    response_data = response.json()
    for item in response_data:
        assert item["city"] in cities


@pytest.mark.parametrize("brewery_type", ["micro", "nano", "regional"])
def test_get_breweries_by_type(base_url_client, brewery_type):
    response = base_url_client.get("/breweries", params={"by_type": brewery_type})
    assert response.ok, response.text
    response_data = response.json()
    for item in response_data:
        assert item["brewery_type"] == brewery_type


@pytest.mark.parametrize("brewery_id", [11767, 11609, 12448])
def test_get_brewery(base_url_client, brewery_id):
    path = f"/breweries/{brewery_id}"
    response = base_url_client.get(path)
    assert response.ok, response.text
    assert response.json()['id'] == brewery_id


@pytest.mark.parametrize("term", ["Kid", "beer", "home"])
def test_autocomplete_brewery(base_url_client, term):
    response = base_url_client.get("/breweries/autocomplete", params={"query": term.lower()})
    assert response.ok, response.text
    response_data = response.json()
    for item in response_data:
        assert list(item.keys()) == ["id", "name"]
    assert len(response_data) <= 15
