import asyncio
from datetime import datetime

import requests
from aiohttp import ClientSession

from iot_server.model.device import DeviceDTO, DeviceSubmittal
from iot_server.model.message import MessageDTO, MessageType


async def main():
    device_uri = setup()
    access_id = 'unknown'

    ws_uri = 'ws://' + device_uri + '/pump/exchange'
    async with ClientSession() as session:
        async with session.ws_connect(ws_uri) as websocket:
            msg: dict = await websocket.receive_json()
            if 'access_id' in msg:
                access_id = msg.get('access_id')

            while True:
                type_ = 'INFO'
                content = f'power: 100% {datetime.now()}'
                target = MessageType.BROADCAST.value
                message = MessageDTO(origin_access_id=access_id, type=type_, content=content, target=target)

                await websocket.send_str(message.json())
                ack = await websocket.receive_str()
                if 'ACK' == ack:
                    print(f'{datetime.now()}: Server acknowledged')
                else:
                    await websocket.close()

                await asyncio.sleep(5)


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
