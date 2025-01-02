from fastapi import HTTPException, status
import httpx
from pymongo import ReturnDocument
from models.transaction import TransactionStatus
from decimal import Decimal
from typing import Optional
import logging

class TransactionService:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)

    async def get_account(self, account_id: str):
        ACCOUNT_SERVICE_URL = "http://localhost:3500/v1.0/invoke/account-service/method/account"
        url = f"{ACCOUNT_SERVICE_URL}/{account_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                try:
                    return response.json()  # Returns account details including the balance
                except ValueError:
                    raise HTTPException(status_code=500, detail="Invalid JSON response from account service")
            else:
                raise HTTPException(status_code=response.status_code, detail="Account not found")
    async def update_account(self, account_id: str, account_data: dict):
    
        ACCOUNT_SERVICE_URL = "http://localhost:3500/v1.0/invoke/account-service/method/account"
        url = f"{ACCOUNT_SERVICE_URL}/{account_id}"

        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=account_data)

            if response.status_code == 200:
                try:
                    print (response.json())
                    return response.json()  # Returns the updated account details
                except ValueError:
                    raise HTTPException(status_code=500, detail="Invalid JSON response from account service")
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Account not found")
            else:
                raise HTTPException(status_code=response.status_code, detail="Failed to update account")
    async def create_transaction_record(self, account_id: str, amount: Decimal, operation: str, transaction_type: str, session: Optional[any] = None):
        # Prepare the transaction document
        transaction_doc = {
            "from_account": account_id,
            "amount": amount,
            "operation": operation,
            "transaction_type": transaction_type,
            "status": TransactionStatus.PENDING,  # Initially set to pending until confirmed
            "timestamp": {"$currentDate": {"timestamp": True}},
        }

        # Insert the transaction record into the transactions collection
        result = await self.db.transactions.insert_one(transaction_doc, session=session)
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create transaction record"
            )
        
        return result.inserted_id

    async def update_account_balance(self, account_id: str, amount: Decimal, operation: str, transaction_type: str, session: Optional[any] = None):
        # Fetch the current balance from the account service
        account = await self.get_account(account_id)
        current_balance= account["balance"]
        # Calculate the modifier based on the operation (credit or debit)
        modifier = 1 if operation == "credit" else -1
        new_balance = current_balance + (amount * modifier)

        # Ensure that the operation does not result in an invalid balance (e.g., negative balance for a debit)
        if new_balance < 0 and operation == "debit":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient funds in account ID: {account_id} for debit operation"
            )
        account["balance"] = new_balance
        # Update the account balance in the account service
        await self.update_account(account_id, account)
        # Create a transaction record
        transaction_id = await self.create_transaction_record(account_id, amount, operation, transaction_type, session)

        # Update the transaction document with the final status (COMPLETED)
        await self.db.transactions.update_one(
            {"_id": transaction_id},
            {"$set": {"status": TransactionStatus.COMPLETED, "final_balance": new_balance}},
            session=session
        )

        # return result

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
                        # Debit the source account and credit the destination account
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "debit",
                            "TRANSFER",
                            session
                        )
                        await self.update_account_balance(
                            transaction_doc["to_account"],
                            transaction_doc["amount"],
                            "credit",
                            "TRANSFER",
                            session
                        )
                    
                    elif transaction_doc["transaction_type"] == "WITHDRAWAL":
                        # Debit the account for a withdrawal
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "debit",
                            "WITHDRAWAL",
                            session
                        )
                    
                    elif transaction_doc["transaction_type"] == "DEPOSIT":
                        # Credit the account for a deposit
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "credit",
                            "DEPOSIT",
                            session
                        )

                    # Mark the transaction as completed and store it in the database
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