from datetime import datetime
from typing import Optional

from mongoengine import StringField, Document, DateTimeField
from pydantic import BaseModel


class DeviceDTO(BaseModel):
    """ A device is a thing that can be everything like a fridge or Raspberry Pi """
    name: str
    place: str
    description: str
    created_at: Optional[datetime]
    update_at: Optional[datetime]

    def to_db(self):
        """ Turns the DTO into a DB object """
        return DeviceDBO(
            name=self.name,
            place=self.place,
            description=self.description,
            created_at=self.created_at,
            update_at=self.update_at
        )


class DeviceDBO(Document):
    name = StringField(required=True, unique=True)
    place = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.now)
    update_at = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'devices',
        'indexes': [
            'name',
            'place',
            'description',
            'created_at',
            'update_at'
        ]
    }

    def to_dto(self) -> DeviceDTO:
        """ Turns the DB object into a DTO """
        return DeviceDTO(
            name=self.name,
            place=self.place,
            description=self.description,
            created_at=self.created_at,
            update_at=self.update_at
        )
