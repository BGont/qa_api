import pytest
import requests


def test_cli_params(url, status_code):
    if url is None:
        pytest.skip("No url was provided")
    response = requests.get(url)
    assert response.status_code == status_code
