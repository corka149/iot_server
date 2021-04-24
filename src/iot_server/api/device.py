""" API collection for device management """
import logging
from typing import List, Optional
from uuid import uuid4

import fastapi
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status, Header
from mongoengine import DoesNotExist
from pydantic import ValidationError

from iot_server.infrastructure.security import authenticated, check_authorization
from iot_server.model.device import DeviceDBO, DeviceDTO, DeviceSubmittal
from iot_server.model.message import MessageDTO, MessageDBO
from iot_server.core import device_service, message_service
from iot_server.core.exchange_service import ExchangeService

router = APIRouter(prefix='/device')
log = logging.getLogger(__name__)
exchange_service = ExchangeService()
DeviceNotFound = HTTPException(
    status_code=fastapi.status.HTTP_404_NOT_FOUND,
    detail='Device not found')


@router.get('', response_model=List[DeviceDTO])
def get_all(_: bool = authenticated) -> List[DeviceDTO]:
    """ Returns all devices """
    devices: List[DeviceDBO] = device_service.get_all_devices()
    return [d.to_dto() for d in devices]


@router.get('/{device_name}', response_model=DeviceDTO)
def get_one(device_name: str, _: bool = authenticated) -> DeviceDTO:
    """ Get one device by its name """
    device: Optional[DeviceDBO] = device_service.get_by_name(device_name)
    if device:
        return device.to_dto()
    raise DeviceNotFound


@router.post('', response_model=DeviceDTO, status_code=fastapi.status.HTTP_201_CREATED)
def create(new_device: DeviceSubmittal, _: bool = authenticated) -> DeviceDTO:
    """ Creates a new device """
    device = device_service.create(new_device.to_db())
    return device.to_dto()


@router.delete('/{device_name}', status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete(device_name: str, _: bool = authenticated):
    """ Deletes a device """
    try:
        device_service.delete(device_name)
    except DoesNotExist:
        # Swallow the DoesNotExist exception
        raise DeviceNotFound from None


@router.put('/{device_name}', response_model=DeviceDTO)
def update(device_name: str, updated_device: DeviceSubmittal, _: bool = authenticated) -> DeviceDTO:
    """ Updates a device excluding name, updated_at and created_at. """
    try:
        device = device_service.update(device_name, updated_device.to_db())
        return device.to_dto()
    except DoesNotExist:
        # Swallow the DoesNotExist exception
        raise DeviceNotFound from None


# Must also have prefix ?!
# _: bool = authenticated <== Not possible o.O ?
@router.websocket('/device/{device_name}/exchange')
async def exchange(websocket: WebSocket, device_name: str,
                   authorization: Optional[str] = Header(None)):
    """ Receives and distribute messages about devices. """
    if check_authorization(authorization):
        log.debug('Successful authenticated')

    device = device_service.get_by_name(device_name)
    if device is None:
        await websocket.close(code=status.WS_1014_BAD_GATEWAY)
        return

    await websocket.accept()
    access_id = str(uuid4())

    exchange_service.register(device_name, access_id, websocket)
    await websocket.send_json({'access_id': access_id})

    try:
        while True:
            message = await _receive_and_convert(websocket)
            if message:
                await exchange_service.dispatch(device_name, access_id, message)
                await websocket.send_text('ACK')
    except WebSocketDisconnect:
        log.warning('client %s disconnected', access_id)
        exchange_service.remove(device_name, access_id)


async def _receive_and_convert(websocket) -> Optional[MessageDTO]:
    json_data = await websocket.receive_json()
    try:
        message = MessageDTO(**json_data)
        message_dbo = MessageDBO(**json_data)
        message_service.create(message_dbo)
        return message
    except ValidationError as ex:
        log.error(str(ex))
        await websocket.send_json(ex.json())
    return None
