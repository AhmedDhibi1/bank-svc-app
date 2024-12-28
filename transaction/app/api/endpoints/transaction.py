from fastapi import APIRouter, Depends, HTTPException, status
from ...db.mongodb import db
from ...models.transaction import TransactionBase, TransactionResponse, TransactionStatus
from ...services.transaction import TransactionService
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

async def get_transaction_service():
    return TransactionService(db.db)

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionBase,
    service: TransactionService = Depends(get_transaction_service)
):
    transaction_doc = {
        "transaction_id": str(uuid.uuid4()),
        "status": TransactionStatus.PENDING,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        **transaction.dict()
    }
    
    result = await service.create_transaction(transaction_doc)
    return TransactionResponse(**result)

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    service: TransactionService = Depends(get_transaction_service)
):
    transaction = await service.db.transactions.find_one({"transaction_id": transaction_id})
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return TransactionResponse(**transaction)

@router.get("/account/{account_id}", response_model=List[TransactionResponse])
async def get_account_transactions(
    account_id: str,
    limit: int = 10,
    skip: int = 0,
    service: TransactionService = Depends(get_transaction_service)
):
    transactions = await service.db.transactions.find(
        {"$or": [
            {"from_account": account_id},
            {"to_account": account_id}
        ]}
    ).sort("created_at", -1).skip(skip).limit(limit).to_list(length=None)
    
    return [TransactionResponse(**tx) for tx in transactions]