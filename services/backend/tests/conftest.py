from typing import Any, Generator

from fastapi.testclient import TestClient
from pytest import fixture

from src.core.jwthandler import create_access_token
from src.main import app as _app


@fixture(scope='module')
def client() -> Generator:
    with TestClient(_app) as client:
        yield client


@fixture(scope='module')
def test_user() -> dict[str, Any]:
    stub = {
        'username': 'test@user.com',
        'full_name': 'Test User',
        'password': 'string',
        'superuser': True,
        'active': True,
    }
    return stub


@fixture(scope='module')
def user_access_token() -> Any:
    return create_access_token({'sub': 'test@user.com'})
