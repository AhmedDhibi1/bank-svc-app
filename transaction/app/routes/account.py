from fastapi import APIRouter, HTTPException
from app.services.account_service import validate_account, update_account_balance
from app.db.schemas import TransactionCreate

router = APIRouter()

@router.post("/validate")
async def validate_account_endpoint(account: TransactionCreate):
    is_valid = await validate_account(account.from_account_id, account.amount, account.transaction_type)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Account validation failed")
    return {"status": "valid"}

@router.put("/update")
async def update_account_balance_endpoint(account: TransactionCreate):
    success = await update_account_balance(account.from_account_id, account.amount, account.transaction_type)
    if not success:
        raise HTTPException(status_code=400, detail="Account update failed")
    return {"status": "updated"}
