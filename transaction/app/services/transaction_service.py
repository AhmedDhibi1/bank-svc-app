from app.db.mongodb import transactions_collection
from app.db.models import insert_transaction, get_transaction_by_id
from app.services.account_service import update_account_balance, validate_account
from app.db.schemas import TransactionCreate, TransactionResponse
from datetime import datetime
from bson import ObjectId

async def create_transaction(transaction: TransactionCreate) -> TransactionResponse:
    # Step 1: Validate the account
    if not await validate_account(transaction.from_account_id, transaction.amount, transaction.transaction_type):
        raise Exception("Insufficient balance or invalid account")

    # Step 2: Create transaction in MongoDB
    transaction_data = transaction.dict()
    transaction_data["status"] = "pending"
    transaction_id = insert_transaction(transaction_data, transactions_collection)

    # Step 3: Update account balances
    if transaction.transaction_type == "debit":
        success = await update_account_balance(transaction.from_account_id, transaction.amount, "debit")
    elif transaction.transaction_type == "credit":
        success = await update_account_balance(transaction.to_account_id, transaction.amount, "credit")

    if not success:
        raise Exception("Failed to update account balance")

    # Step 4: Update transaction status
    transactions_collection.update_one(
        {"_id": ObjectId(transaction_id)},
        {"$set": {"status": "completed"}}
    )

    transaction_data["transaction_id"] = str(transaction_id)
    return TransactionResponse(**transaction_data)

async def get_transaction_by_id(transaction_id: str) -> TransactionResponse:
    transaction = get_transaction_by_id(transaction_id, transactions_collection)
    if not transaction:
        return None
    transaction["transaction_id"] = str(transaction["_id"])
    return TransactionResponse(**transaction)
