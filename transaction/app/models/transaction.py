import uuid
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
    amount: float = Field(..., gt=0)
    transaction_type: TransactionType
    from_account: uuid.UUID
    to_account: Optional[uuid.UUID] = None
    description: Optional[str] = None

class TransactionResponse(TransactionBase):
    transaction_id: uuid.UUID
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime