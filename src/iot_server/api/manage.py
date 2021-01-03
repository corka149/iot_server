from fastapi import APIRouter


router = APIRouter(prefix='/manage')


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.get('/info')
def info():
    return {'status': 'ok'}
