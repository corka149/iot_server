""" Securing the IoT server. """

import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from iot_server.infrastructure import config

security = HTTPBasic()


def is_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Must be used as dependency. It will return only true when the correct
    basic auth is provided.
    """
    username = config.get_config('security.basic.username')
    passwd = config.get_config('security.basic.password')

    correct_user = secrets.compare_digest(credentials.username, username)
    correct_passwd = secrets.compare_digest(credentials.password, passwd)

    if not (correct_user and correct_passwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return True


authenticated = Depends(is_authenticated)
""" States that the request passed the basic authentication check. """
