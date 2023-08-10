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
        response = client.get(f'/api/v1/users/{random.randint(1, 100)}')
        assert response.status_code == 404
        assert response.json() == {
            'error': True,
            'message': 'User not found',
            'code': 1,
        }

    response = client.get(f'/api/v1/users?page=1&page_size=20')
    assert response.status_code == 200
    assert response.json()['error'] == False
    assert response.json()['page'] == 1
    assert response.json()['page_size'] == 20
    assert response.json()['users'] == []

def test_create():
    created_users = []
    for id in range(NUM_TESTS):
        response = client.post('/api/v1/users/create', json={
            'email': f'{"".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(random.randint(1, 15))])}@{"".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(random.randint(1, 4))])}.ru',
            'password': f'{"".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(random.randint(1, 15))])}',
        })

        print(response.json())
        assert response.status_code == 200
        created_users.append(response.json())
        assert created_users[-1]['error'] == False
        assert created_users[-1]['id'] == id + 1
        assert created_users[-1]['is_banned'] == False
        assert created_users[-1]['balance'] == 0

        response2 = client.get(f'/api/v1/users/{id + 1}')
        assert response2.status_code == 200
        response2 = response2.json()
        assert response2['error'] == False
        assert response2['id'] == id + 1
        assert response2['email'] == created_users[-1]['email']
        assert response2['is_banned'] == False

    response = client.post('/api/v1/users/create', json={
        'email': 'test@example.com',
        'password': 'test',
    })
    response2 = client.post('/api/v1/users/create', json={
        'email': 'test@example.com',
        'password': 'another_password',
    })
    assert response2.status_code == 400
    assert response2.json() == {
        'error': True,
        'message': 'User already exists',
        'code': 2,
    }

def test_404():
    for _ in range(NUM_TESTS):
        random_id = random.randint(200, 500)
        response = client.get(f'/api/v1/users/{random_id}')
        assert response.status_code == 404
        assert response.json() == {
            'error': True,
            'message': 'User not found',
            'code': 1
        }

def test_edit():
    response = client.post('/api/v1/users/create', json={
        'email': 'testing_email_10@popusk.heh',
        'password': 'test',
    })
    user_data = response.json()
    user_id = user_data['id']
    edit_response = client.put(f'/api/v1/users/{user_id}/edit', json={
        'password': 'test',
        'new_password': 'test',
        'new_email': 'testing_email_11@popusk.heh',
    })
    assert edit_response.status_code == 200
    user_data = client.get(f'/api/v1/users/{user_id}').json()
    assert user_data['email'] == 'testing_email_11@popusk.heh'

    edit_response = client.put(f'/api/v1/users/{user_id}/edit', json={
        'password': 'test',
        'new_password': 'test2',
        'new_email': 'testing_email_11@popusk.heh',
    })
    edit_response = client.put(f'/api/v1/users/{user_id}/edit', json={
        'password': 'test',
        'new_password': 'test2',
        'new_email': 'testing_email_11@popusk.heh',
    })
    assert edit_response.status_code == 403
    assert edit_response.json() == {
        'error': True,
        'message': 'Invalid password',
        'code': 4,
    }