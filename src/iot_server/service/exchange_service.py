""" Exchange message between devices """
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

from starlette.websockets import WebSocket

from iot_server.model.message import MessageDTO, MessageType


class ExchangeService:
    """ Tiny websocket broadcaster that store in memory websocket connections. """
    _connections: Dict[str, List[Tuple[str, WebSocket]]] = defaultdict(list)
    _log = logging.getLogger('ExchangeService')

    @classmethod
    def register(cls, device_name: str, access_id: str, websocket: WebSocket):
        """ Registers a new websocket connection. """
        cls._connections[device_name].append((access_id, websocket))
        cls._log.info('%d registered access ids for device %s', len(cls._connections[device_name]), device_name)

    @classmethod
    def remove(cls, device_name: str, access_id: str):
        """ Removes a websocket connection from the connection store. """
        cls._log.info('Removed access id "%s" for device "%s" (%d register devices)',
                      access_id, device_name, len(cls._connections[device_name]))

        new_sockets = [(a_id, ws) for a_id, ws
                       in cls._connections[device_name] if a_id != access_id]
        cls._connections[device_name] = new_sockets

    @classmethod
    async def dispatch(cls, device_name: str, sender_id: str, message: MessageDTO):
        """ Dispatches a message to 0, 1 or n targets """
        is_broadcast = message.target == MessageType.BROADCAST.value

        cls._log.info('%d potential targets for message', len(cls._connections[device_name]))
        for access_id, web_socket in cls._connections[device_name]:
            web_socket: WebSocket = web_socket
            if is_broadcast and access_id != sender_id:
                cls._log.info('Send message to access id "%s"', access_id)
                await web_socket.send_text(message.json())
            elif access_id == message.target:
                # Must be single target
                cls._log.info('Send message to access id "%s"', access_id)
                await web_socket.send_text(message.json())
                return
