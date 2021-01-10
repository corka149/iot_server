from fastapi.testclient import TestClient

from iot_server.main import api

test_client: TestClient = TestClient(api)


def test_get_all():
    response = test_client.get('/device')
    assert response.status_code == 200
