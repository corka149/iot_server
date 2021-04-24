import aioredis

from iot_server.core.exchange_service import ExchangeService
from iot_server.infrastructure import config


async def exchange_service():
    host = config.get_config('redis.host')
    port = config.get_config('redis.port')
    password = config.get_config('redis.password')
    database = config.get_config('redis.database')

    url = f'redis://{host}:{port}'
    pool = await aioredis.create_redis_pool(
        url, db=database, password=password
    )

    exchange_svc = ExchangeService(pool)
    return exchange_svc
