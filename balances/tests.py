import os
import requests
from fastapi import testclient

import main

client = testclient.TestClient(main.app)

NUM_TESTS = 25

def test_create():
    for id_ in range(NUM_TESTS):
        response = client.post('/api/v1/balances/create', json={
            'user_id': id_ + 1,
        })

        assert response.status_code == 200
        assert response.json()['error'] == False
        assert response.json()['points'] == 0