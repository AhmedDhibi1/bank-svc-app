from fastapi import APIRouter, HTTPException
from app.services.transaction_service import create_transaction, get_transaction_by_id
from app.db.schemas import TransactionCreate, TransactionResponse

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
async def create_transaction_endpoint(transaction: TransactionCreate):
    try:
        return await create_transaction(transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_endpoint(transaction_id: str):
    transaction = await get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction