from fastapi.testclient import TestClient

from .server import app

client = TestClient(app)

def test_read_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Pong!"}

if __name__ == '__main__':
    test_read_ping()
