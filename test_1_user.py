import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

client = TestClient(app)

def get_valid_headers():
    response = client.get("/token/new-test-token")
    valid_headers = {"Authorization": f"Bearer {response.json()['token']}"}
    return valid_headers

# Test creating a new user
def test_create_user_success():
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+916367296133"
    }
    response = client.post("/users/", json=data, headers=get_valid_headers())
    print(response)
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

def test_create_user_validation_error():
    data = {
        "name": "John Doe",
        "email": "invalid-email",
        "phone": "invalid-phone"
    }
    response = client.post("/users/", json=data, headers=get_valid_headers())
    assert response.status_code == 422

# Test retrieving a user
def test_get_user_success():
    response = client.get("/users/1", headers=get_valid_headers())  # Replace with valid user ID
    assert response.status_code == 200
    assert "name" in response.json()

def test_get_user_not_found():
    response = client.get("/users/9999", headers=get_valid_headers())
    assert response.status_code == 404
    assert response.json() == {"detail": "User not Found"}

# Test updating user details
def test_update_user_success():
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "+1234567891"
    }
    response = client.put("/users/1", json=data, headers=get_valid_headers())  # Replace with valid user ID
    assert response.status_code == 202
    assert response.json()["name"] == "Jane Doe"

def test_update_user_not_found():
    data = {
        "name": "Non-existent User",
        "email": "nonexistent@example.com",
        "phone": "+0000000000"
    }
    response = client.put("/users/9999", json=data, headers=get_valid_headers())
    assert response.status_code == 404
    assert response.json() == {"detail": "User not Found"}
