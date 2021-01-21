""" Exceptions that occur on device side. """
from datetime import datetime

from mongoengine import Document, StringField, DateTimeField
from pydantic.main import BaseModel


class ExceptionDBO(Document):
    """ Stored exception """
    hostname = StringField()
    clazz = StringField()
    message = StringField()
    stacktrace = StringField()
    created_at = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'exceptions',
        'indexes': [
            'hostname',
            'clazz',
            'message',
            'stacktrace',
            'created_at'
        ]
    }


class ExceptionSubmittal(BaseModel):
    """ New not persisted exception. It has a hostname, clazz, message, stacktrace. """
    hostname: str
    clazz: str
    message: str
    stacktrace: str

    def to_db(self) -> ExceptionDBO:
        """ Turns the DTO into a DB object """
        return ExceptionDBO(
            hostname=self.hostname,
            clazz=self.clazz,
            message=self.message,
            stacktrace=self.stacktrace
        )
