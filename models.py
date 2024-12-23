from typing import Annotated, Optional, Union
from pydantic import EmailStr, AfterValidator
import phonenumbers
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import event
from enum import Enum

#* Enumerations
class TransactionTypeEnum(Enum):
    CREDIT = "credit"
    DEBIT = "debit"

    @classmethod
    def from_value(cls, value: str):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid transaction type. Allowed types: {', '.join([e.value for e in cls])}")


#* Validators  
def validate_phone(value):
    try:
        parsed_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number format")
    return value

#* Base Classes
class BaseTable(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UserBase(SQLModel):
    name: str
    email: EmailStr
    phone: Annotated[str, AfterValidator(validate_phone)]    

class WalletBase(SQLModel):
    balance: Optional[float] = 0
    user_id: int = Field(foreign_key="user.id")

class TransactionBase(SQLModel):
    transaction_type: Annotated[str, AfterValidator(TransactionTypeEnum.from_value)]
    amount: float
    description: Optional[str] = ""



#* Table Classes
class User(UserBase, BaseTable, table=True):
    wallet: Union["Wallet", None] = Relationship(back_populates="user")

class Wallet(WalletBase, BaseTable, table=True):
    user: User = Relationship(back_populates="wallet")
    #TODO: How to do one to many
    transaction: Union["Transaction", None] = Relationship(back_populates="origin_wallet")

class Transaction(TransactionBase, BaseTable, table=True):
    wallet_id: int = Field(foreign_key="wallet.id")
    origin_wallet: Wallet = Relationship(back_populates="transaction")

#* Schemas
class CreateUser(UserBase):
    ...

class UpdateUser(SQLModel):
    name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""

class CreateWallet(WalletBase):
    ...

class CreateTransaction(TransactionBase):
    ...