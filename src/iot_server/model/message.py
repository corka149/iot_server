""" Messages are exchanged between connected devices. """
from datetime import datetime
from enum import Enum

from mongoengine import Document, StringField, DateTimeField
from pydantic import BaseModel


class MessageType(Enum):
    """Type of an incoming message"""

    BROADCAST = "BROADCAST"
    SERVER = "SERVER"


class MessageDBO(Document):
    """Message model in database"""

    type = StringField()
    target = StringField()
    content = StringField()
    origin_access_id = StringField()
    timestamp = DateTimeField(default=datetime.now)

    meta = {"collection": "messages", "indexes": ["type", "content", "timestamp"]}


class MessageDTO(BaseModel):
    """To be exchanged between devices"""

    origin_access_id: str
    type: str
    target: str
    content: str
