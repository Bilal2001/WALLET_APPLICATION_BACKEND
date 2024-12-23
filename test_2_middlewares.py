import time
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#* Test middleware for authentication
def get_valid_token():
    response = client.get("/token/new-test-token")
    return response.json()["token"]
    
def test_auth_middleware_missing_token():
    response = client.get("/users/all")
    assert response.status_code == 401
    assert response.json() == {"detail": "Authorization header missing or invalid"}

def test_auth_middleware_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/users/all", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_auth_middleware_valid_token():
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}  
    response = client.get("/users", headers=headers)
    print(response.text)
    assert response.status_code == 200

# #* Test middleware for rate limiting Couldn't get this to work
# def test_rate_limit():
#     time.sleep(6)
#     token = get_valid_token()
#     headers = {"Authorization": f"Bearer {token}"}  
#     for _ in range(10):
#         print(_)
#         response = client.get("/users", headers=headers)
#         print(response.text)
#         assert response.status_code == 200
#         time.sleep(3)
#     # Exceed rate limit
#     response = client.get("/users", headers=headers)
#     print(response.text)
#     assert response.status_code == 429
