from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Amount in UZS")
    type: TransactionType
    category: str
    date: datetime = Field(default_factory=datetime.now)
    note: Optional[str] = None
    source: Optional[str] = "Plastik karta"


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: str
    model_config = ConfigDict(from_attributes=True)


class CreateTransactionResponse(BaseModel):
    transaction: Transaction
    round_up: Optional[Any] = None
