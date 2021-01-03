import os

import mongoengine
import uvicorn
from fastapi import FastAPI

api = FastAPI()


def configure_database():
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_port = os.getenv('DB_PORT', 27017)
    db_username = os.getenv('DB_USERNAME', 'admin')
    db_password = os.getenv('DB_PASSWORD', 's3cr3t')
    mongoengine.connect('iot', host=db_host, port=db_port, username=db_username, password=db_password,
                        authentication_source='admin')


def configure_routes():
    from iot_server.api import manage, device
    api.include_router(manage.router)
    api.include_router(device.router)


def configure():
    configure_database()
    configure_routes()


if __name__ == '__main__':
    # from IDE
    configure()
    uvicorn.run(api)
else:
    configure()
