import main
import app
import pytest
import httpx
from app import views

views.destroy_models()
views.init_models()

client = httpx.AsyncClient(app=main.app, base_url=f'http://127.0.0.1:17012{app.PREFIX}')

@pytest.mark.anyio
@pytest.mark.order(1)
async def test_health_check():
    # print(os.environ.get('DB_HOST'), init.DATABASE_URL)

    response = await client.get('users/health')
    print(response.url, response.status_code, response.content)

    assert response.status_code == 200
    assert not response.json()['error']

@pytest.mark.anyio
@pytest.mark.order(2)
async def test_user_not_found():
    response = await client.get('users/1000')
    assert response.status_code == 404

    response_json = response.json()
    assert response_json['error'] == True
    assert response_json['code'] == 1
    assert response_json['message'] == 'User not found'

@pytest.mark.anyio
@pytest.mark.order(3)
async def test_get_users():
    response = await client.get('users')
    print(response.url, response.status_code, response.content)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['error'] == False
    assert response_json['page'] == 1
    assert response_json['page_size'] == 20
    assert response_json['users'] == []

@pytest.mark.anyio
@pytest.mark.order(4)
async def test_create():
    response = await client.post('users/create', json={
        'email': 'sam_takoy@ti_tupoy.com',
        'password': 'Loohi123',
    })
    assert response.status_code == 201

    response_json = response.json()
    assert response_json['error'] == False
    assert response_json['id'] == 1
    assert response_json['email'] == 'sam_takoy@ti_tupoy.com'
    assert response_json['is_banned'] == False
    assert response_json['balance'] == 0

@pytest.mark.anyio
@pytest.mark.order(5)
async def test_create_existing_user():
    response = await client.post('users/create', json={
        'email': 'sam_takoy@ti_tupoy.com',
        'password': 'Loohi123',
    })
    assert response.status_code == 400

    response_json = response.json()
    assert response_json['error'] == True
    assert response_json['code'] == 2
    assert response_json['message'] == 'User already exists'

@pytest.mark.anyio
@pytest.mark.order(6)
async def test_getting_user():
    response = await client.get('users/1')
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['error'] == False
    assert response_json['id'] == 1
    assert response_json['email'] == 'sam_takoy@ti_tupoy.com'
    assert response_json['is_banned'] == False
    assert response_json['balance'] == 0

@pytest.mark.anyio
@pytest.mark.order(7)
async def test_getting_users():
    response = await client.get('users/')
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['error'] == False
    assert response_json == {
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
