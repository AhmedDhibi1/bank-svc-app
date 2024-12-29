from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float
    transaction_type: str  # debit or credit

class TransactionResponse(TransactionCreate):
    transaction_id: str
    timestamp: datetime
    status: str  # "pending", "completed", "failed"

    class Config:
        orm_mode = True
