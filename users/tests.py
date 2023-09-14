from fastapi import testclient
import main
import init
import os

client = testclient.TestClient(main.app)

def test_health_check():
    '''Test of health check'''
    # print(os.environ.get('DB_HOST'), init.DATABASE_URL)

    response = client.get(f'{init.PREFIX}/users/health_check')

    assert response.status_code == 200
    assert not response.json()['error']

def test_create_and_read():
    '''Test of creating and reading user'''

    # Testing getting single user
    response = client.get(f'{init.PREFIX}/users/1000')
    assert response.status_code == 404

    response_json = response.json()
    assert response_json['error'] == True
    assert response_json['code'] == 1
    assert response_json['message'] == 'User not found'

    # Testing getting multiple users
    response = client.get(f'{init.PREFIX}/users')
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['error'] == False
    assert response_json['page'] == 1
    assert response_json['page_size'] == 20
    assert response_json['users'] == []

    # Testing user creating (main case)
    responce = client.get(f'{init.PREFIX}/users/create', json={
        'email': 'sam_takoy@ti_tupoy.com',
        'password': 'Loohi123',
    })
    assert responce.status_code == 201

    response_json = response.json()
    assert response_json['error'] == False
    assert response_json['id'] == 1
    assert response_json['email'] == 'sam_takoy@ti_tupoy.com'
    assert response_json['is_banned'] == False
    assert response_json['balance'] == 0

    # Testing user creating (user already exists)
    responce = client.post(f'{init.PREFIX}/users/create', json={
        'email': 'sam_takoy@ti_tupoy.com',
        'password': 'Loohi123',
    })
    assert responce.status_code == 400

    response_json = response.json()
    assert response_json['error'] == True
    assert response_json['code'] == 2
    assert response_json['message'] == 'User already exists'

    # Testing getting user
    responce = client.get(f'{init.PREFIX}/users/1')
    assert responce.status_code == 200

    response_json = responce.json()
    assert response_json['error'] == False
    assert response_json['id'] == 1
    assert response_json['email'] == 'sam_takoy@ti_tupoy.com'
    assert response_json['is_banned'] == False
    assert response_json['balance'] == 0

    # Testing getting users
    responce = client.get(f'{init.PREFIX}/users/')
    assert responce.status_code == 200

    responce_json = responce.json()
    assert responce_json['error'] == False
    assert responce_json == {
        'error': False,
        'page': 1,
        'page_size': 20,
        'users': [
            {
                'id': 1,
                'email': 'sam_takoy@ti_tupoy.com',
                'is_banned': False,
                'balance': 0
            }
        ],
    }
