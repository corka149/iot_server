import asyncio

import requests
import websockets

from iot_server.model.device import DeviceDTO, DeviceSubmittal
from iot_server.model.message import MessageDTO


async def main():
    device_uri = setup()

    ws_uri = 'ws://' + device_uri + '/pump/exchange'
    async with websockets.connect(ws_uri) as websocket:
        while True:
            type_ = input('Type: ').strip()
            content = input('Content: ').strip()
            message = MessageDTO(type=type_, content=content)
            await websocket.send(message.json())


def setup():
    device_uri = '127.0.0.1:8000/device'
    response = requests.get('http://' + device_uri + '/pump')
    if response.status_code == 200:
        _ = DeviceDTO(**response.json())
        print('Received device data')
    else:
        device_sub = DeviceSubmittal(name='pump', place='garden', description='For water')
        response = requests.post('http://' + device_uri, data=device_sub.json())
        response.raise_for_status()
        _ = DeviceDTO(**response.json())
        print('Created device data')
    return device_uri


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
