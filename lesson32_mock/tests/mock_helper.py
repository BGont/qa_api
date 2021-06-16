from unittest.mock import Mock


def mock_client(base_url=None):

    test_client = Mock(**{"base_url": base_url})
    test_client.ok.return_value = True
    test_client.text = "Ошибка"
    test_client.get.return_value = test_client
    test_client.post.return_value = test_client
    test_client.put.return_value = test_client
    test_client.patch.return_value = test_client
    test_client.delete.return_value = test_client

    return test_client
