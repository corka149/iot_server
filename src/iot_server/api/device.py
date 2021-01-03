from typing import List, Optional

import fastapi
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist

from iot_server.model import device_service
from iot_server.model.device import DeviceDBO, DeviceDTO

router = APIRouter(prefix='/device')
DeviceNotFound = HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail='Device not found')


@router.get('', response_model=List[DeviceDTO])
def get_all() -> List[DeviceDTO]:
    """ Returns all devices """
    devices: List[DeviceDBO] = device_service.get_all_devices()
    return [d.to_dto() for d in devices]


@router.get('/{device_name}', response_model=DeviceDTO)
def get_one(device_name: str) -> DeviceDTO:
    """ Get one device by its name """
    device: Optional[DeviceDBO] = device_service.get_by_name(device_name)
    if device:
        return device.to_dto()
    raise DeviceNotFound


@router.post('', response_model=DeviceDTO, status_code=fastapi.status.HTTP_201_CREATED)
def create(new_device: DeviceDTO) -> DeviceDTO:
    """ Creates a new device """
    device = device_service.create(new_device.to_db())
    return device.to_dto()


@router.delete('/{device_name}', status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete(device_name: str):
    """ Deletes a device """
    try:
        device_service.delete(device_name)
    except DoesNotExist:
        raise DeviceNotFound


@router.put('/{device_name}', response_model=DeviceDTO)
def update(device_name: str, updated_device: DeviceDTO) -> DeviceDTO:
    """ Updates a device excluding name, updated_at and created_at. """
    device: DeviceDBO = DeviceDBO.objects(name=device_name).first()
    if device is None:
        raise DeviceNotFound
    device.place = updated_device.place
    device.description = updated_device.description
    device = device.save()
    return device.to_dto()
