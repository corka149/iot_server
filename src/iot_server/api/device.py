from typing import List, Optional

import fastapi
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist

from iot_server.model.device import DeviceDBO, DeviceDTO, DeviceSubmittal
from iot_server.service import device_service

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
def create(new_device: DeviceSubmittal) -> DeviceDTO:
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
def update(device_name: str, updated_device: DeviceSubmittal) -> DeviceDTO:
    """ Updates a device excluding name, updated_at and created_at. """
    try:
        device = device_service.update(device_name, updated_device.to_db())
        return device.to_dto()
    except DoesNotExist:
        raise DeviceNotFound
