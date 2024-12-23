from datetime import datetime
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from database import get_session
from models import CreateWallet, Wallet, User, CreateTransaction, Transaction, TransactionTypeEnum
from uuid import uuid4

SIGN = {
    "credit": 1,
    "debit": -1
}
LIMIT = 10

app = APIRouter(prefix="/wallets", tags=["wallets"])

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_wallet(
    wallet_data: CreateWallet,
    session: Session = Depends(get_session)
) -> Wallet:
    #* Check if user with user_id exists
    user_data = session.exec(select(User).where(User.id == wallet_data.user_id)).first()
    if user_data is None:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    
    #* Check if wallet for user id exists (single wallet)
    wallet_instance = session.exec(select(Wallet).where(Wallet.user_id == wallet_data.user_id)).first()
    if wallet_instance is not None:
        return JSONResponse(status_code=404, content={"detail": "Wallet for user already exists"})
    
    wallet = Wallet(
        user_id=wallet_data.user_id,
        balance=wallet_data.balance
    )
    session.add(wallet)
    session.commit()
    session.refresh(wallet)
    return wallet

@app.post("/{wallet_id}/transactions", status_code=status.HTTP_201_CREATED)
async def perform_transaction(
    wallet_id: int,
    transaction_data: CreateTransaction,
    session: Session = Depends(get_session)
):
    #* Check if wallet exists
    wallet = session.exec(select(Wallet).where(Wallet.id == wallet_id)).first()
    if wallet is None:
        return JSONResponse(status_code=404, content={"detail": "Wallet not found"})
    
    #* Check if amount can be debited
    if transaction_data.transaction_type.value == "debit" and \
        wallet.balance < transaction_data.amount:
        return JSONResponse(status_code=404, content={"detail": "Wallet has insufficient balance"})

    #* Set Description
    default_description = f"{transaction_data.transaction_type.value.capitalize()}ing {transaction_data.amount}"
    description = transaction_data.description \
                  if len(transaction_data.description)   \
                  else default_description
    
    transaction = Transaction(
        transaction_type = transaction_data.transaction_type.value,
        amount = transaction_data.amount,
        description = description,
        wallet_id = wallet_id
    )

    #* Update Wallet Balance
    wallet.balance += (SIGN[transaction_data.transaction_type.value] * transaction_data.amount)
    wallet.updated_at = datetime.now()

    #* Add all and Commit
    session.add_all([transaction, wallet])
    session.commit()
    session.refresh(transaction)
    return transaction

@app.get("/{wallet_id}/balance", status_code=status.HTTP_200_OK)
async def get_wallet_balance(
    wallet_id: int,
    session: Session = Depends(get_session)
):
    #* Check if wallet exists
    wallet = session.exec(select(Wallet).where(Wallet.id == wallet_id)).first()
    if wallet is None:
        return JSONResponse(status_code=404, content={"detail": "Wallet not found"})
    
    return wallet

@app.get("/{wallet_id}/transactions", status_code=status.HTTP_200_OK)
async def get_wallet_transactions(
    wallet_id: int, 
    page_number: int = 1,
    per_page: int = LIMIT,
    session: Session = Depends(get_session)
):
    #* Check if wallet exists
    wallet = session.exec(select(Wallet).where(Wallet.id == wallet_id)).first()
    if wallet is None:
        return JSONResponse(status_code=404, content={"detail": "Wallet not found"})
    
    #* Validate pagination arguments
    if page_number < 1 or per_page < 1:
        return JSONResponse(status_code=404, content={"detail": "Invalid Pagination Arguments"})
    
    limit = per_page
    offset = (page_number - 1) * per_page
    transactions = session.exec(select(Transaction) \
                   .where(Transaction.wallet_id == wallet_id) \
                   .limit(limit).offset(offset)).all()
    return transactions
    


# #* Testing
@app.get("/wallets", status_code=status.HTTP_200_OK)
async def get_wallets(session: Session = Depends(get_session)):
    return session.exec(select(Wallet)).all()

@app.get("/transactions", status_code=status.HTTP_200_OK)
async def get_wallets(session: Session = Depends(get_session)):
    return session.exec(select(Transaction)).all()