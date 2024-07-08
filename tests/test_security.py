from datetime import datetime, timedelta
from http import HTTPStatus

from jwt import decode, encode
from zoneinfo import ZoneInfo

from fast_zero.security import create_access_token, settings


def test_jwt():
    data = {'sub': 'test@example.com'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['sub'] == data['sub']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_without_sub_clain(client):
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTOS
    )

    to_encode = {'sub': None, 'exp': expire}

    token = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_invalid_username(client):
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTOS
    )
    to_encode = {'sub': 'invalid@mail.com', 'exp': expire}

    token = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
