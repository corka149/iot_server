from fastapi.testclient import TestClient

from iot_server.main import app

test_client: TestClient = TestClient(app)


def test_health():
    response = test_client.get(
        '/manage/health', auth=('iotTest', 'passwdTest'))
    assert 200 == response.status_code


def test_info():
    response = test_client.get('/manage/info', auth=('iotTest', 'passwdTest'))
    assert 200 == response.status_code
