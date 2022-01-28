from datetime import datetime
from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.database import Database

client = TestClient(app)
db = Database()

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Social-Media-API is working."
    assert response.json().get("source_code") == "https://github.com/Devansh3712/social-media-api"

def test_create_user():
    user = {
        "username": "test",
        "password": "test",
        "timestamp": str(datetime.now())
    }
    response = client.post("/users/", json = user)
    db.delete("test", user)
    assert response.status_code == 201
    assert response.json().get("username") == user["username"]
