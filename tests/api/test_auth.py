import json

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_create_user(client, get_user_from_db):
    payload = {
        'name': 'Вася',
        'surname': 'Пупкин',
        'email': 'create_user@kek.ru',
        'password': 'user123qwe'
    }
    response: Response = client.post('/auth/registration/', content=json.dumps(payload))
    assert response.status_code == 201
    answer = response.json()
    assert len(answer) == 5
    assert payload['name'] == answer['name']
    assert payload['surname'] == answer['surname']
    assert payload['email'] == answer['email']
    assert isinstance(answer['user_id'], int)
    assert answer['user_uuid']

    user = get_user_from_db(answer['user_id'])
    assert user['password'] != payload['password']
    for key, val in answer.items():
        assert key in user and val == user[key]

    response: Response = client.post('/auth/registration/', content=json.dumps(payload))
    assert response.status_code == 422
    assert response.json() == {'detail': 'Пользователь с таким email уже существует'}


@pytest.mark.asyncio
async def test_login(client, get_refresh_token_from_db):
    payload = {
        'name': 'Вася',
        'surname': 'Пупкин',
        'email': 'user_login@mail.ru',
        'password': 'user123qwe'
    }
    client.post('/auth/registration/', content=json.dumps(payload))
    response: Response = client.post(
        '/auth/login/',
        content=json.dumps(
            {
                'email': payload['email'],
                'password': payload['password']
            }
        )
    )
    assert response.status_code == 200
    assert response.json()['access_token']

    token = response.cookies.get('refresh_token')
    assert token
    refresh_token = get_refresh_token_from_db(token)
    assert refresh_token

    response: Response = client.post(
        '/auth/login/',
        content=json.dumps(
            {
                'email': 'not_found@ddd.ru',
                'password': '3er32fdsac23'
            }
        )
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Неверный логин или пароль'}
    assert response.cookies.get('refresh_token') is None

    response: Response = client.post(
        '/auth/login/',
        content=json.dumps(
            {
                'email': 'user_login@mail.ru',
                'password': 'bad_password'
            }
        )
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Неверный логин или пароль'}
    assert response.cookies.get('refresh_token') is None


@pytest.mark.asyncio
async def test_is_auth(client):
    payload = {
        'name': 'Вася',
        'surname': 'Пупкин',
        'email': 'is_auth@mail.ru',
        'password': 'user123qwe'
    }
    client.post('/auth/registration/', content=json.dumps(payload))
    response_login: Response = client.post(
        '/auth/login/',
        content=json.dumps({'email': payload['email'], 'password': payload['password']})
    )
    resp_is_auth: Response = client.get(
        '/auth/isAuth/',
        headers={'access-token': response_login.json()['access_token']}
    )
    assert resp_is_auth.status_code == 200
    assert resp_is_auth.json()['user_id']

    resp_is_auth: Response = client.get(
        '/auth/isAuth/',
        headers={'access-token': 'bad_token'}
    )
    assert resp_is_auth.status_code == 401
    assert resp_is_auth.json() == {'detail': "Невалидный токен"}