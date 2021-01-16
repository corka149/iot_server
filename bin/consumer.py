import asyncio
from datetime import datetime

import aiohttp
from aiohttp import ClientSession, WSMessage


async def main():
    async with ClientSession() as session:
        async with session.ws_connect('http://127.0.0.1:8000/device/pump/exchange') as websocket:
            print('Connected')
            async for msg in websocket:
                msg: WSMessage = msg
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(f'{datetime.now()}: Server sent "{msg.data}"')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('ERROR')
                    break


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
