""" Service for management of device exceptions """

from iot_server.model.exception import ExceptionDBO


def create(new_exception: ExceptionDBO) -> ExceptionDBO:
    """ Creates a new exception in database. """
    return new_exception.save()
