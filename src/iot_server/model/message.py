import uuid
from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, UUIDField
from pydantic import BaseModel


class MessageDBO(Document):
    """ Message model in database """
    id = UUIDField(default=uuid.uuid4)
    type = StringField()
    content = StringField()
    timestamp = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'messages',
        'indexes': [
            'type',
            'content',
            'timestamp'
        ]
    }


class MessageDTO(BaseModel):
    """ To be exchanged between devices """
    type: str
    content: str
