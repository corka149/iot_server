""" Management API """
from fastapi import APIRouter


router = APIRouter(prefix='/manage')


@router.get('/health')
def health():
    """ States the health of the service. """
    return {'status': 'ok'}


@router.get('/info')
def info():
    """ Shares info about the service instance. """
    return {'status': 'ok'}
