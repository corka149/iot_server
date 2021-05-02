""" Main entrypoint for API service """
import logging.config
import os

import mongoengine
import uvicorn
from fastapi import FastAPI

from iot_server.api import manage, device, exception
from iot_server.infrastructure import config

app = FastAPI(debug=True)
logger = logging.getLogger("iot_server")


def configure_database():
    """Configures everything around the database on the startup."""
    host = config.get_config("database.host")

    # Test profile uses mock mongo db
    if os.getenv("IOT_SERVER_PROFILE", "test") == "test":
        mongoengine.connect("iot", host=host)
    else:
        port = config.get_config("database.port")
        username = config.get_config("database.username")
        password = config.get_config("database.password")
        authentication_source = config.get_config("database.authentication_source")
        mongoengine.connect(
            "iot",
            host=host,
            port=port,
            username=username,
            authentication_source=authentication_source,
            password=password,
        )


def configure_routes():
    """Configures the routes for the FastAPI app."""
    app.include_router(manage.router)
    app.include_router(device.router)
    app.include_router(exception.router)


def configure(profile=None):
    """Central configuration entrypoint."""
    profile = profile if profile else os.getenv("IOT_SERVER_PROFILE", "test")
    config.init(profile)
    configure_database()
    configure_routes()


@app.on_event("startup")
def start_up():
    profile = os.getenv("IOT_SERVER_PROFILE", "test")
    logger.info("PROFILE: %s", profile)


if __name__ == "__main__":
    # from IDE
    configure("dev")

    log_config = config.logging()

    uvicorn.run(app, log_config=log_config)
else:
    configure()
