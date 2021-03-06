""" Main entrypoint for API service """
import logging
import os

import mongoengine
import uvicorn
from fastapi import FastAPI

from iot_server.api import manage, device, exception
from iot_server.infrastructure import config

api = FastAPI(debug=True)
logger = logging.getLogger(__name__)


def configure_database():
    """ Configures everything around the database on the startup. """
    db_conf = config.get_config('database')
    mongoengine.connect('iot', **db_conf)


def configure_routes():
    """ Configures the routes for the FastAPI app. """
    api.include_router(manage.router)
    api.include_router(device.router)
    api.include_router(exception.router)


def configure(profile=None):
    """ Central configuration entrypoint. """
    profile = profile if profile else os.getenv('IOT_SERVER_PROFILE', 'test')
    logger.info('PROFILE: %s', profile)
    config.init(profile)
    configure_database()
    configure_routes()


if __name__ == '__main__':
    # from IDE
    configure('dev')
    uvicorn.run(api)
else:
    configure()
