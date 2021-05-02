""" Exchange message between devices """
import asyncio
import logging
from collections import defaultdict
from typing import List, Any

import aioredis
from aioredis import Redis
from starlette.websockets import WebSocket

from iot_server.model.message import MessageDTO, MessageType

STREAM = "iot_messages"
LAST_ID = "$"


class PoolBoy:
    """Takes care about Redis connection pool"""

    _instance = None
    _pool: Redis

    def __new__(cls, host: str, port: int, db: str, password: str):
        if not cls._instance:
            cls._instance = super(cls, PoolBoy).__new__(cls)

            cls._instance._port = port
            cls._instance._host = host
            cls._instance._password = password
            cls._instance._db = db
            cls._instance._pool = None

        return cls._instance

    @property
    async def pool(self) -> Redis:
        if not self._pool:
            self._pool = await aioredis.create_redis_pool(
                f"redis://{self._host}:{self._port}",
                encoding="utf8",
                password=self._password,
                db=self._db,
            )

        return self._pool


class ExchangeService:
    """Exchanges message between processes."""

    _log = logging.getLogger(__name__)
    _instance = None
    _task_launched: bool

    def __new__(cls, pool_boy: PoolBoy):
        if not cls._instance:
            cls._instance = super(cls, ExchangeService).__new__(cls)

            cls._instance._connections = defaultdict(dict)
            cls._instance._boy = pool_boy
            cls._task_launched = False

        return cls._instance

    def register(self, device_name: str, access_id: str, websocket: WebSocket):
        """Registers a new websocket connection."""
        device_name = device_name.lower().strip()
        self._log.info('Register id %s for "%s"', access_id, device_name)
        self._connections[device_name][access_id] = websocket
        self._log_stats()

        # Listening makes only sense when someone registered
        if not self._task_launched:
            self._log.info("Registered listen-task")
            asyncio.get_event_loop().create_task(self._instance.listen())
            self._task_launched = True

    def remove(self, device_name: str, access_id: str):
        """Removes a websocket connection from the connection store."""
        self._log.info("Remove id %s from %s", access_id, device_name)
        del self._connections[device_name][access_id]
        self._log_stats()

    async def dispatch(self, device_name: str, sender_id: str, message: MessageDTO):
        """Dispatches a message."""
        # Inform other workers
        pool = await self._boy.pool

        payload = {
            **message.dict(),
            "device_name": device_name,
            "sender_id": sender_id,
        }

        await pool.xadd(STREAM, payload, max_len=5)

    async def listen(self):
        """Listens endless for messages from io message stream and distribute them."""
        pool = await self._boy.pool
        while True:
            payloads = pool.xread([STREAM], latest_ids=[LAST_ID], timeout=0, count=1)
            deliveries = list()

            for payload in await payloads:
                self._log.info("Received %r", payload)

                device_name = payload.get("device_name")
                sender_id = payload.get("sender_id")
                message = MessageDTO(**payload)

                is_broadcast = message.target == MessageType.BROADCAST.value

                deliveries = deliveries + (
                    self._distribute_message(
                        device_name, is_broadcast, message, sender_id
                    )
                )

            await asyncio.gather(*deliveries)

    # ===== PRIVATE =====

    def _distribute_message(
        self, device_name, is_broadcast, message, sender_id
    ) -> List[Any]:
        """Delivers a single message to all possible receivers"""
        deliveries = list()

        for access_id, web_socket in self._connections[device_name].items():
            web_socket: WebSocket = web_socket
            if is_broadcast and access_id != sender_id:
                self._log.info('Send message to access id "%s"', access_id)
                deliveries.append(web_socket.send_text(message.json()))
            elif access_id == message.target:
                # Must be single target
                self._log.info('Send message to access id "%s"', access_id)
                deliveries.append(web_socket.send_text(message.json()))
                break

        return deliveries

    # ===== PRIVATE =====

    def _log_stats(self):
        self._log.info('Connections hold by "%d"', id(self._connections))
        for key in self._connections:
            ids = self._connections[key].keys()
            self._log.info("Registered ids for %s: %s", key, ", ".join(ids))
