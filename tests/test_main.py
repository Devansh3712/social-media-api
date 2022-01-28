from datetime import datetime
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Social-Media-API is working."
    assert response.json().get("source_code") == "https://github.com/Devansh3712/social-media-api"
