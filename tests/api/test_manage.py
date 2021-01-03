from fastapi.testclient import TestClient

from iot_server.main import api

test_client: TestClient = TestClient(api)


def test_health():
    response = test_client.get('/manage/health')
    assert response.status_code == 200


def test_info():
    response = test_client.get('/manage/info')
    assert response.status_code == 200
