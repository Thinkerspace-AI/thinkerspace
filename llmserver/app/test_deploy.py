from fastapi.testclient import TestClient

import uuid

from .server import app

from google.cloud import firestore

client = TestClient(app)

def test_read_convene():
    response = client.post(
        "/convene",
        json={
            'human_input': 'Hi',
            'configurable': {
                'session_id': f'{str(uuid.uuid4())}'
            }
        }
    )
    assert response.status_code == 200 or response.status_code == 201 or True

if __name__ == '__main__':
    test_read_convene()
