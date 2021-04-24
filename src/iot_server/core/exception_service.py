""" Service for management of device exceptions """
from typing import Optional

from iot_server.model.exception import ExceptionDBO


def create(new_exception: ExceptionDBO) -> ExceptionDBO:
    """ Creates a new exception in database. """
    return new_exception.save()


def get_one(exception_id: str) -> Optional[ExceptionDBO]:
    """ Get a exception from DB by its id. """
    return ExceptionDBO.objects(id=exception_id).first()
