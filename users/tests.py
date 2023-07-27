import random
import os
import models
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import Depends
from main import app, get_db

client = TestClient(app)

NUM_TESTS = 25

def test_get():
    for _ in range(NUM_TESTS):
        responce = client.get(f'/users/{random.randint(1, 100)}')
        assert responce.status_code == 404
        assert responce.json() == {
            'error': True,
            'message': 'User not found',
            'code': 1,
        }

    responce = client.get(f'/users?page=1&page_size=20')
    assert responce.status_code == 200
    assert responce.json()['error'] == False
    assert responce.json()['page'] == 1
    assert responce.json()['page_size'] == 20
    assert responce.json()['users'] == []

def test_create():
    created_users = []
    for id in range(NUM_TESTS):
        responce = client.post('/users/create', json={
            'email': f'{"".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(random.randint(1, 15))])}@{"".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(random.randint(1, 4))])}.ru',
            'password': f'{"".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(random.randint(1, 15))])}',
        })
        assert responce.status_code == 200
        created_users.append(responce.json())
        assert created_users[-1]['error'] == False
        assert created_users[-1]['id'] == id + 1
        assert created_users[-1]['is_banned'] == False

        responce2 = client.get(f'/users/{id + 1}')
        assert responce2.status_code == 200
        responce2 = responce2.json()
        assert responce2['error'] == False
        assert responce2['id'] == id + 1
        assert responce2['email'] == created_users[-1]['email']
        assert responce2['is_banned'] == False

    responce = client.post('/users/create', json={
        'email': 'test@example.com',
        'password': 'test',
    })
    responce2 = client.post('/users/create', json={
        'email': 'test@example.com',
        'password': 'another_password',
    })
    assert responce2.status_code == 400
    assert responce2.json() == {
        'error': True,
        'message': 'User already exists',
        'code': 2,
    }

def test_404():
    for _ in range(NUM_TESTS):
        random_id = random.randint(200, 500)
        responce = client.get(f'/users/{random_id}')
        assert responce.status_code == 404
        assert responce.json() == {
            'error': True,
            'message': 'User not found',
            'code': 1
        }

def test_edit():
    responce = client.post('/users/create', json={
        'email': 'testing_email_10@popusk.heh',
        'password': 'test',
    })
    user_data = responce.json()
    user_id = user_data['id']
    edit_responce = client.put(f'/users/{user_id}/edit', json={
        'password': 'test',
        'new_password': 'test',
        'new_email': 'testing_email_11@popusk.heh',
    })
    assert edit_responce.status_code == 200
    user_data = client.get(f'/users/{user_id}').json()
    assert user_data['email'] == 'testing_email_11@popusk.heh'

    edit_responce = client.put(f'/users/{user_id}/edit', json={
        'password': 'test',
        'new_password': 'test2',
        'new_email': 'testing_email_11@popusk.heh',
    })
    edit_responce = client.put(f'/users/{user_id}/edit', json={
        'password': 'test',
        'new_password': 'test2',
        'new_email': 'testing_email_11@popusk.heh',
    })
    assert edit_responce.status_code == 403
    assert edit_responce.json() == {
        'error': True,
        'message': 'Invalid password',
        'code': 4,
    }