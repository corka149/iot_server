""" Exception report endpoint for devices """

import logging

import fastapi
from fastapi import APIRouter

from iot_server.model.exception import ExceptionSubmittal
from iot_server.service import exception_service

router = APIRouter(prefix='/exception')
log = logging.getLogger(__name__)


@router.post('', status_code=fastapi.status.HTTP_201_CREATED)
def create(new_exception: ExceptionSubmittal) -> str:
    """ Creates a new exception occurrence and returns the id of the new stored exception. """
    ex = exception_service.create(new_exception.to_db())
    return str(ex.id)