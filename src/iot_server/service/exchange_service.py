""" Exchange message between devices """
from collections import defaultdict
from typing import Dict, List

from starlette.websockets import WebSocket

from iot_server.model.message import MessageDTO


class ExchangeService:
    _connections: Dict[str, List[WebSocket]] = defaultdict(list)

    @classmethod
    def register(cls, device_name: str, websocket: WebSocket):
        cls._connections[device_name].append(websocket)

    @classmethod
    def remove(cls, device_name: str, websocket: WebSocket):
        cls._connections.get(device_name, []).remove(websocket)

    @classmethod
    async def broadcast(cls, device_name: str, sender: WebSocket, message: MessageDTO):
        for ws in cls._connections.get(device_name, []):
            if ws != sender:
                await ws.send_json(message)
