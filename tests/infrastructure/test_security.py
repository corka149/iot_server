from fastapi import HTTPException

from iot_server.infrastructure import security, config


def test_check_authorization():
    # Prepare
    config.init('test')

    # Check
    assert security.check_authorization('Basic aW90VGVzdDpwYXNzd2RUZXN0')

    failed = False
    try:
        security.check_authorization('blub')
    except HTTPException:
        failed = True

    assert failed
