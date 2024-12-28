from fastapi import HTTPException, status
from pymongo import ReturnDocument
from ..models.transaction import TransactionStatus
from decimal import Decimal
from typing import Optional

class TransactionService:
    def __init__(self, db):
        self.db = db

    async def update_account_balance(
        self, 
        account_id: str, 
        amount: Decimal, 
        operation: str,
        session: Optional[any] = None
    ):
        modifier = 1 if operation == "credit" else -1
        result = await self.db.accounts.find_one_and_update(
            {"_id": account_id, "balance": {"$gte": -amount if operation == "debit" else 0}},
            {"$inc": {"balance": amount * modifier}},
            session=session,
            return_document=ReturnDocument.AFTER
        )
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds or account not found"
            )
        return result

    async def create_transaction(self, transaction_doc):
        try:
            async with await self.db.client.start_session() as session:
                async with session.start_transaction():
                    # Process based on transaction type
                    if transaction_doc["transaction_type"] == "TRANSFER":
                        if not transaction_doc["to_account"]:
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="To account is required for transfers"
                            )
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "debit",
                            session
                        )
                        await self.update_account_balance(
                            transaction_doc["to_account"],
                            transaction_doc["amount"],
                            "credit",
                            session
                        )
                    
                    elif transaction_doc["transaction_type"] == "WITHDRAWAL":
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "debit",
                            session
                        )
                    
                    elif transaction_doc["transaction_type"] == "DEPOSIT":
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "credit",
                            session
                        )

                    transaction_doc["status"] = TransactionStatus.COMPLETED
                    await self.db.transactions.insert_one(transaction_doc, session=session)

        except Exception as e:
            transaction_doc["status"] = TransactionStatus.FAILED
            await self.db.transactions.insert_one(transaction_doc)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        return transaction_doc