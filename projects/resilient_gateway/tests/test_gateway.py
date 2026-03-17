from fastapi.testclient import TestClient
import os
import sys

# Add subproject to path
subproject_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, subproject_path)
sys.path.insert(0, os.path.dirname(subproject_path))

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_simulation_complete():
    payload = {
        "prompt": "Hello",
        "model": "gpt-4o"
    }
    response = client.post("/v1/complete", json=payload)
    assert response.status_code == 200
    assert "Simulated response" in response.json()["text"]
