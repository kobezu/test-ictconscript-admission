from fastapi.testclient import TestClient
import sys
sys.path.append('../app')
from main import app


"""These tests use sample logs in sample-data/data.json as test data"""

client = TestClient(app)

# Respond with proper log entry when requested   
def test_read_entry_success():
  response = client.get("/entries/1")
  assert response.status_code == 200
  assert response.json() == {
    "id": "1",
    "title": "Night perimeter check",
    "body": "All clear around main gate.",
    "isoTime": "2025-05-14T21:30:00Z",
    "lat": 60.1503,
    "lon": 25.0293
  }

# List all log entries when requested
def test_list_entries():
  response = client.get("/entries")
  assert response.status_code == 200

  entries = response.json()
  assert isinstance(entries, list)
  assert len(entries) == 10 # Sample dataset has 10 entries

# Create a new log entry successfully
def test_create_entry_success():
    payload = {
      "title": "Test entry",
      "body": "Post request should succeed and return matching entry",
      "lat": 42.1503,
      "lon": 23.0293
    }
    response = client.post("/entries", json=payload)
    assert response.status_code == 200

    created_entry = response.json()
    assert created_entry["title"] == payload["title"]
    assert created_entry["body"] == payload["body"]
    assert created_entry["lat"] == payload["lat"]
    assert created_entry["lon"] == payload["lon"]

# Respond with proper status code and message when accessing non-existent entry
def test_read_entry_failure():
  response = client.get("/entries/1000")
  assert response.status_code == 404
  assert response.json() == {"detail": "Entry 1000 not found"}

# Respond with proper status code when POST request has incorrect format
def test_post_entry_failure():
  payload = {
    "title": "Body is missing",
    "lat": 42.1503,
    "lon": 23.0293
  }
  response = client.post("/entries", json=payload)
  assert response.status_code == 422