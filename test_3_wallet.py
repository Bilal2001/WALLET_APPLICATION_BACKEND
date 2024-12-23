import time
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_valid_headers():
    response = client.get("/token/new-test-token")
    valid_headers = {"Authorization": f"Bearer {response.json()['token']}"}
    return valid_headers

# Test creating a wallet
def test_create_wallet_success():
    data = {"user_id": 1, "balance": 1000.0}  # Replace with a valid user ID
    response = client.post("/wallets/", json=data, headers=get_valid_headers())
    assert (response.status_code == 201 and response.json()["balance"] == 1000.0) \
        or (response.status_code == 404 and response.json() == {"detail": "Wallet for user already exists"})

def test_create_wallet_user_not_found():
    data = {"user_id": 9999, "balance": 500.0}  # Replace with an invalid user ID
    response = client.post("/wallets/", json=data, headers=get_valid_headers())
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# Test retrieving wallet balance
def test_get_wallet_balance_success():
    time.sleep(5)
    response = client.get("/wallets/1/balance", headers=get_valid_headers())  # Replace with a valid wallet ID
    assert response.status_code == 200
    assert "balance" in response.json()

def test_get_wallet_balance_not_found():
    response = client.get("/wallets/9999/balance", headers=get_valid_headers())
    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}
