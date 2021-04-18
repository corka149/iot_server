from fastapi.testclient import TestClient

from iot_server.main import app
from iot_server.model.device import DeviceDBO, DeviceDTO, DeviceSubmittal
from iot_server.service import device_service

test_client: TestClient = TestClient(app)


def test_get_all():
    device = DeviceDBO(name='bubble', place='kitchen',
                       description='Brings light')
    device_service.create(device)

    response = test_client.get('/device', auth=('iotTest', 'passwdTest'))
    assert 200 == response.status_code

    json_response = response.json()
    device_dtos = [DeviceDTO(**d) for d in json_response]

    assert 1 <= len(device_dtos)
    assert any([device.name == d.name for d in device_dtos])


def test_get():
    device = DeviceDBO(name='fridge', place='kitchen', description='For food')
    device_service.create(device)

    response = test_client.get(
        '/device/' + device.name, auth=('iotTest', 'passwdTest'))
    assert 200 == response.status_code

    dto = DeviceDTO(**response.json())
    assert device.name == dto.name
    assert device.place == dto.place
    assert device.description == dto.description


def test_create():
    device = DeviceSubmittal(
        name='freezer', place='Kitchen', description='So cool')

    response = test_client.post(
        '/device', data=device.json(), auth=('iotTest', 'passwdTest'))
    assert 201 == response.status_code

    created_device = DeviceDTO(**response.json())
    assert device.name == created_device.name
    assert device.place == created_device.place
    assert device.description == created_device.description


def test_update():
    device = DeviceDBO(name='Toaster', place='kitchen',
                       description='Makes toast')
    device = device_service.create(device)

    update = DeviceSubmittal(
        name='toaster', place='second kitchen', description='why not?')
    response = test_client.put(
        '/device/' + device.name, data=update.json(), auth=('iotTest', 'passwdTest'))
    assert 200 == response.status_code

    device = device_service.get_by_name(device.name)
    assert device.name == update.name
    assert device.place == update.place
    assert device.description == update.description


def test_delete():
    device = DeviceDBO(name='stove', place='kitchen',
                       description='Kitchen again')
    device_service.create(device)

    response = test_client.delete(
        '/device/STOVE', auth=('iotTest', 'passwdTest'))
    assert 204 == response.status_code

    device = device_service.get_by_name(device.name)
    assert device is None
