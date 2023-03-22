import json

import pytest
from fastapi import Response


@pytest.mark.asyncio
async def test_create_user(client):
    payload = {
        'name': 'user',
        'surname': 'user',
        'email': 'lol@kek.ru',
        'password': 'user123qwe'
    }
    response: Response = client.post('/auth/registration/', data=json.dumps(payload))
    assert response.status_code == 201
    assert len(response.json()) == 5
    assert payload['name'] == response.json()['name']
    assert payload['surname'] == response.json()['surname']
    assert payload['email'] == response.json()['email']
    assert payload['password'] != response.json()['password']
    assert response.json()['user_id']

    response: Response = client.post('/auth/registration/', data=json.dumps(payload))
    assert response.status_code == 422
    assert response.json() == {'detail': 'Пользователь с таким email уже существует'}
