from fastapi import testclient
import main
import init

client = testclient.TestClient(main.app)

def health_check_test():
    '''Test of health check'''
    response = client.get(f'{init.PREFIX}/users/health_check')

    assert response.status_code == 200
    assert response.json()['error'] == False