""" Exchange message between devices """
import logging
from collections import defaultdict
from typing import Dict

from starlette.websockets import WebSocket

from iot_server.model.message import MessageDTO, MessageType


class ExchangeService:
    """ Tiny websocket broadcaster that store in memory websocket connections. """
    _connections: Dict[str, Dict[str, WebSocket]] = defaultdict(dict)
    _log = logging.getLogger('ExchangeService')

    @classmethod
    def register(cls, device_name: str, access_id: str, websocket: WebSocket):
        """ Registers a new websocket connection. """
        cls._log.info('Register id %s for %s', access_id, device_name)
        cls._connections[device_name][access_id] = websocket
        cls._log_stats()

    @classmethod
    def remove(cls, device_name: str, access_id: str):
        """ Removes a websocket connection from the connection store. """
        cls._log.info('Remove id %s from %s', access_id, device_name)
        del cls._connections[device_name][access_id]
        cls._log_stats()

    @classmethod
    async def dispatch(cls, device_name: str, sender_id: str, message: MessageDTO):
        """ Dispatches a message to 0, 1 or n targets """
        is_broadcast = message.target == MessageType.BROADCAST.value

        cls._log_stats()

        for access_id, web_socket in cls._connections[device_name].items():
            web_socket: WebSocket = web_socket
            if is_broadcast and access_id != sender_id:
                cls._log.info('Send message to access id "%s"', access_id)
                await web_socket.send_text(message.json())
            elif access_id == message.target:
                # Must be single target
                cls._log.info('Send message to access id "%s"', access_id)
                await web_socket.send_text(message.json())
                return

    @classmethod
    def _log_stats(cls):
        cls._log.info('Connections hold by "%d"', id(cls._connections))
        for key in cls._connections:
            ids = cls._connections[key].keys()
            cls._log.info('Registered ids for %s: %s', key, ', '.join(ids))
