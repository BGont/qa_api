import pytest
import requests
from urllib.parse import urljoin


class TestClient(requests.Session):
    __test__ = False

    def __init__(self, base_url):
        super(TestClient, self).__init__()
        self.base_url = base_url

    def request(self, method, path,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):
        url = urljoin(self.base_url, path)

        return super().request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )


@pytest.fixture(scope="session")
def test_client(request):
    TestClient.mock_tests = request.config.getoption("--mock_tests")
    return TestClient


def pytest_addoption(parser):
    parser.addoption("--url", help="Request URL")
    parser.addoption("--status_code", default=200, type=int, help="Status code")
    parser.addoption("--mock_tests", default=False, action="store_true",
                     help="Mock actual requests to external api")


@pytest.fixture(scope="function")
def url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope="function")
def status_code(request):
    return request.config.getoption("--status_code")
