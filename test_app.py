import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_register_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "Test Customer",
            "email": "test@example.com"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Test Customer"
    assert data["email"] == "test@example.com"