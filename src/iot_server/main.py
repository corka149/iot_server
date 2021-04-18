""" Main entrypoint for API service """
import logging
import os

import mongoengine
import uvicorn
from fastapi import FastAPI

from iot_server.api import manage, device, exception
from iot_server.infrastructure import config

app = FastAPI(debug=True)
logger = logging.getLogger(__name__)


def configure_database():
    """ Configures everything around the database on the startup. """
    host = config.get_config('database.host')

    # Test profile uses mock mongo db
    if os.getenv('IOT_SERVER_PROFILE', 'test') == 'test':
        mongoengine.connect('iot', host=host)
    else:
        port = config.get_config('database.port')
        username = config.get_config('database.username')
        password = config.get_config('database.password')
        authentication_source = config.get_config(
            'database.authentication_source')
        mongoengine.connect('iot', host=host, port=port, username=username,
                            authentication_source=authentication_source,
                            password=password)


def configure_routes():
    """ Configures the routes for the FastAPI app. """
    app.include_router(manage.router)
    app.include_router(device.router)
    app.include_router(exception.router)


def configure(profile=None):
    """ Central configuration entrypoint. """
    profile = profile if profile else os.getenv('IOT_SERVER_PROFILE', 'test')
    logger.info('PROFILE: %s', profile)
    config.init(profile)
    configure_database()
    configure_routes()


@app.on_event('startup')
def on_startup():
    config.set_log_level(config.get_config('logging.level'))


if __name__ == '__main__':
    # from IDE
    configure('dev')
    uvicorn.run(app)
else:
    configure()
