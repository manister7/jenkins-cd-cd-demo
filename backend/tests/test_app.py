import pytest
from backend.app import app
@pytest.fixture

def client():
    app.testing = True
    return app.test_client()

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"welcome to the Public API Demo" in response.data

def test_dog_route(client):
    response = client.get("/dog")
    assert response.status_code == 200
    data = response.get_json()
    assert "image_url" in data
    assert data["status"] == "success"

def test_dog_html_route(client):
    response = client.get("/dog/html")
    assert response.status_code == 200
    assert b"<h1>Random Dog</h1>" in response.data