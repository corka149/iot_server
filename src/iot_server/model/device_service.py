from typing import List, Optional

from iot_server.model.device import DeviceDBO


def get_all_devices() -> List[DeviceDBO]:
    return list(DeviceDBO.objects())


def get_by_name(device_name: str) -> Optional[DeviceDBO]:
    return DeviceDBO.objects(name=device_name).first()


def create(device: DeviceDBO) -> DeviceDBO:
    return device.save()


def delete(device_name: str):
    device: DeviceDBO = DeviceDBO.objects(name=device_name).get()
    device.delete()
