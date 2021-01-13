import asyncio

import websockets


async def main():
    async with websockets.connect('ws://127.0.0.1:8000/device/pump/exchange') as websocket:
        print('Connected')
        async for data in websocket:
            print(f'==> {data}')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
