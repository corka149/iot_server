""" Exceptions that occur on device side. """

from mongoengine import Document, StringField
from pydantic.main import BaseModel


class ExceptionDBO(Document):
    """ Stored exception """
    hostname = StringField()
    clazz = StringField()
    message = StringField()
    stacktrace = StringField()

    meta = {
        'collection': 'exceptions',
        'indexes': [
            'hostname',
            'clazz',
            'message',
            'stacktrace'
        ]
    }


class ExceptionSubmittal(BaseModel):
    """ New not persisted exception """
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
