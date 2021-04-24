""" Exchange message between devices """
import logging
from collections import defaultdict
from typing import Dict, Optional

import aioredis
from aioredis import Redis
from starlette.websockets import WebSocket

from iot_server.infrastructure import config
from iot_server.model.message import MessageDTO, MessageType


STREAM = 'iot_messages'


class PoolBoy:
    """ Takes care about Redis connection pool """

    def __init__(self, host: str, port: int, db: str, password: str):
        self._port = port
        self._host = host
        self._password = password
        self._db = db
        self._pool: Optional[Redis] = None

    @property
    async def pool(self) -> Redis:
        if not self._pool:
            self._pool = await aioredis.create_redis_pool(
                f'redis://{self._host}:{self._port}', encoding='utf8',
                password=self._password, db=self._db
            )

        return self._pool


class ExchangeService:
    """ Exchanges message between processes. """
    _log = logging.getLogger('ExchangeService')
    _instance = None

    def __init__(self, pool_boy: PoolBoy):
        self._connections: Dict[str, Dict[str, WebSocket]] = defaultdict(dict)
        self._boy: Optional[PoolBoy] = pool_boy

    def register(self, device_name: str, access_id: str, websocket: WebSocket):
        """ Registers a new websocket connection. """
        device_name = device_name.lower().strip()
        self._log.info('Register id %s for "%s"', access_id, device_name)
        self._connections[device_name][access_id] = websocket
        self._log_stats()

    def remove(self, device_name: str, access_id: str):
        """ Removes a websocket connection from the connection store. """
        self._log.info('Remove id %s from %s', access_id, device_name)
        del self._connections[device_name][access_id]
        self._log_stats()

    async def dispatch(self, device_name: str, sender_id: str, message: MessageDTO):
        """ Dispatches a message to 0, 1 or n targets """
        is_broadcast = message.target == MessageType.BROADCAST.value

        self._log_stats()

        for access_id, web_socket in self._connections[device_name].items():
            web_socket: WebSocket = web_socket
            if is_broadcast and access_id != sender_id:
                self._log.info('Send message to access id "%s"', access_id)
                await web_socket.send_text(message.json())
            elif access_id == message.target:
                # Must be single target
                self._log.info('Send message to access id "%s"', access_id)
                await web_socket.send_text(message.json())
                return

    # ===== PRIVATE =====

    def _log_stats(self):
        self._log.info('Connections hold by "%d"', id(self._connections))
        for key in self._connections:
            ids = self._connections[key].keys()
            self._log.info('Registered ids for %s: %s', key, ', '.join(ids))
