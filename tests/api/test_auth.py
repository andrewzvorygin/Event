import json

import pytest
from fastapi import Response


@pytest.mark.asyncio
async def test_create_user(client, get_user_from_db):
    payload = {
        'name': 'user',
        'surname': 'user',
        'email': 'lol@kek.ru',
        'password': 'user123qwe'
    }
    response: Response = client.post('/auth/registration/', data=json.dumps(payload))
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

    response: Response = client.post('/auth/registration/', data=json.dumps(payload))
    assert response.status_code == 422
    assert response.json() == {'detail': 'Пользователь с таким email уже существует'}
