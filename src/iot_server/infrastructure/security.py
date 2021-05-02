""" Securing the IoT server. """
import base64
import logging
import secrets
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from iot_server.infrastructure import config

""" Central security """
security = HTTPBasic()

""" User could not authenticated """
FailedLogin = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Basic"},
)

_LOG = logging.getLogger(__name__)


def is_authenticated(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Must be used as dependency. It will return only true when the correct
    basic auth is provided.
    """
    if not __is_authenticated(credentials.username, credentials.password):
        raise FailedLogin

    return True


def check_authorization(auth_header_value: Optional[str]) -> bool:
    """
    Checks the authorization header by auth header.

    :param auth_header_value: Auth header value
    :return: successful authenticated?
    """
    try:
        # Right authentication method?
        if auth_header_value and auth_header_value[:6] == "Basic ":
            b64 = auth_header_value.lstrip("Basic").strip()
            decrypted_b64 = base64.decodebytes(bytes(b64, "ascii"))
            credentials = str(decrypted_b64, encoding="ascii")

            # Right format?
            if credentials.count(":") == 1:
                username, password = credentials.split(":")

                # Correct credentials ?
                if __is_authenticated(username, password):
                    return True
            else:
                _LOG.error('Illegal credentials format: "%s"', credentials)
        else:
            _LOG.error("Not basic auth header")
    except Exception as ex:
        _LOG.error("Exception while checking basic auth: %s", ex)
    raise FailedLogin


def __is_authenticated(username: str, password: str) -> bool:
    conf_username = config.get_config("security.basic.username")
    conf_passwd = config.get_config("security.basic.password")

    correct_user = secrets.compare_digest(username, conf_username)
    correct_passwd = secrets.compare_digest(password, conf_passwd)

    return correct_user and correct_passwd


authenticated = Depends(is_authenticated)
""" States that the request passed the basic authentication check. """
