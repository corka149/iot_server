""" Exchange message between devices """
import logging
from collections import defaultdict
from typing import Dict

from aioredis import Redis
from starlette.websockets import WebSocket

from iot_server.model.message import MessageDTO, MessageType


class ExchangeService:
    """ Tiny websocket broadcaster that store in memory websocket connections. """
    _log = logging.getLogger('ExchangeService')

    def __init__(self, pool: Redis = None):
        self._pool: Redis = pool
        self._connections: Dict[str, Dict[str, WebSocket]] = defaultdict(dict)

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

    def _log_stats(self):
        self._log.info('Connections hold by "%d"', id(self._connections))
        for key in self._connections:
            ids = self._connections[key].keys()
            self._log.info('Registered ids for %s: %s', key, ', '.join(ids))
