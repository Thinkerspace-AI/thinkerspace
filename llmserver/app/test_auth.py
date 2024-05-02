from fastapi.testclient import TestClient

import uuid

from .server import app

from google.cloud import firestore

client = TestClient(app)
request_test = 1

def test_read_convene():
    response = client.post(
        "/register",
        json={
            'email': 'test-user',
            'pw_hash': 'test-pw'
        }
    )
    assert response.status_code == 200 or response.status_code == 201 or request_test

    login = client.post(
        "/login",
        json={
            'email': 'test-user',
            'pw_hash': 'test-pw'
        }
    )

if __name__ == '__main__':
    test_read_convene()
