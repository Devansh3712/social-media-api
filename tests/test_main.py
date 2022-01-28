from datetime import datetime
from fastapi.testclient import TestClient
from src.main import app
from src.database import Database

client = TestClient(app)
db = Database()

user = {
    "username": "test",
    "password": "test"
}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Social-Media-API is working."
    assert response.json().get("source_code") == "https://github.com/Devansh3712/social-media-api"

def test_create_user():
    response = client.post("/users/", json = user)
    db.database["test"].drop()
    assert response.status_code == 201
    assert response.json().get("username") == user["username"]

def test_get_user():
    client.post("/users/", json = user)
    response = client.get("/users/test/", data = user)
    db.database["test"].drop()
    assert response.status_code == 200
    assert response.json().get("username") == user["username"]

def test_login_user():
    client.post("/users/", json = user)
    response = client.post("/login", data = user)
    db.database["test"].drop()
    assert response.status_code == 200
    assert response.json().get("token_type") == "bearer"
