import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_valid_headers():
    response = client.get("/token/new-test-token")
    valid_headers = {"Authorization": f"Bearer {response.json()['token']}"}
    return valid_headers

# Test performing a transaction
def test_perform_transaction_success():
    data = {
        "transaction_type": "credit",
        "amount": 500.0,
        "description": "Test credit transaction"
    }
    response = client.post("/wallets/1/transactions", json=data, headers=get_valid_headers())  # Replace with a valid wallet ID
    assert response.status_code == 201
    assert response.json()["amount"] == 500.0

def test_perform_transaction_insufficient_balance():
    data = {
        "transaction_type": "debit",
        "amount": 2000.0,  # Ensure this exceeds the wallet's balance
        "description": "Test debit transaction"
    }
    response = client.post("/wallets/1/transactions", json=data, headers=get_valid_headers())  # Replace with a valid wallet ID
    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet has insufficient balance"}

def test_perform_transaction_wallet_not_found():
    data = {
        "transaction_type": "credit",
        "amount": 500.0,
        "description": "Test transaction for non-existent wallet"
    }
    response = client.post("/wallets/9999/transactions", json=data, headers=get_valid_headers())
    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}
