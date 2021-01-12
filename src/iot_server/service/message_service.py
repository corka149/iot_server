""" Manager of messages """
import uuid
from typing import List, Optional

from iot_server.model.message import MessageDBO


def get_all_messages() -> List[MessageDBO]:
    """ Get all messages from database. """
    return list(MessageDBO.objects())


def get_by_name(message_id: uuid.UUID) -> Optional[MessageDBO]:
    """ Get a message by name from database. """
    return MessageDBO.objects(name=message_id).first()


def create(message: MessageDBO) -> MessageDBO:
    """ Creates a new message in database. """
    return message.save()


def delete(message_id: uuid.UUID):
    """ Deletes a message from database. """
    message: MessageDBO = MessageDBO.objects(name=message_id).get()
    message.delete()
