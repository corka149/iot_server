""" Management API """
from fastapi import APIRouter

from iot_server.infrastructure.security import authenticated

router = APIRouter(prefix="/manage")


@router.get("/health")
def health(_: bool = authenticated):
    """States the health of the service."""
    return {"status": "ok"}


@router.get("/info")
def info(_: bool = authenticated):
    """Shares info about the service instance."""
    return {"status": "ok"}
