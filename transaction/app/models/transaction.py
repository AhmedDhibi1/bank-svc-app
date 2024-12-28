from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"

class TransactionBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    transaction_type: TransactionType
    from_account: str
    to_account: Optional[str] = None
    description: Optional[str] = None

class TransactionResponse(TransactionBase):
    transaction_id: str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime