from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"
    assert "env" in data


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
