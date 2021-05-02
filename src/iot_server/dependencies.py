from fastapi import Depends

from iot_server.core.exchange_service import ExchangeService, PoolBoy
from iot_server.infrastructure import config


def get_pool_boy():
    """Creates a new pool boy"""

    return PoolBoy(
        host=config.get_config("redis.host"),
        port=config.get_config("redis.port"),
        db=config.get_config("redis.db"),
        password=config.get_config("redis.password"),
    )


def get_exchange(pool_boy=Depends(get_pool_boy)):
    """Creates a new exchange service"""

    return ExchangeService(pool_boy)
