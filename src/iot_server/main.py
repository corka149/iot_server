import logging
import os

import mongoengine
import uvicorn
from fastapi import FastAPI

from iot_server.infrastructure import config

api = FastAPI()
logger = logging.getLogger(__name__)


def configure_database():
    db_conf = config.get_config('database')
    mongoengine.connect('iot', **db_conf)


def configure_routes():
    from iot_server.api import manage, device
    api.include_router(manage.router)
    api.include_router(device.router)


def configure(profile=None):
    profile = profile if profile else os.getenv('IOT_SERVER_PROFILE', 'test')
    logger.info('PROFILE: ' + profile)
    config.init(profile)
    configure_database()
    configure_routes()


if __name__ == '__main__':
    # from IDE
    configure('dev')
    uvicorn.run(api)
else:
    configure()
