""" Manager of devices """
from datetime import datetime
from typing import List, Optional

from iot_server.model.device import DeviceDBO


def get_all_devices() -> List[DeviceDBO]:
    """Get all devices from database."""
    return list(DeviceDBO.objects())


def get_by_name(device_name: str) -> Optional[DeviceDBO]:
    """Get a device by name from database."""
    device_name = device_name.lower().strip()
    return DeviceDBO.objects(name=device_name).first()


def create(device: DeviceDBO) -> DeviceDBO:
    """Creates a new device in database."""
    device.name = device.name.lower().strip()
    return device.save()


def delete(device_name: str):
    """Deletes a device from database."""
    device_name = device_name.lower().strip()
    device: DeviceDBO = DeviceDBO.objects(name=device_name).get()
    device.delete()


def update(device_name: str, updated_device: DeviceDBO) -> DeviceDBO:
    """Updates a device in database."""
    device_name = device_name.lower().strip()
    device: DeviceDBO = DeviceDBO.objects(name=device_name).get()
    device.place = updated_device.place
    device.description = updated_device.description
    device.update_at = datetime.now()
    device = device.save()
    return device
