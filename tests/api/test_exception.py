from fastapi.testclient import TestClient

from iot_server.main import app
from iot_server.model.exception import ExceptionSubmittal
from iot_server.service import exception_service

test_client: TestClient = TestClient(app)


def test_create():
    dto = ExceptionSubmittal(
        hostname='some-raspberry-pi',
        clazz=ValueError.__name__,
        message='Value not allowed',
        stacktrace='foo bar'
    )

    response = test_client.post(
        '/exception', data=dto.json(), auth=('iotTest', 'passwdTest'))

    assert response.status_code == 201
    assert 0 < len(response.text)

    dbo = exception_service.get_one(response.text)
    assert dbo
    assert dbo.hostname == dto.hostname
    assert dbo.clazz == dto.clazz
    assert dbo.message == dto.message
    assert dbo.stacktrace == dto.stacktrace
