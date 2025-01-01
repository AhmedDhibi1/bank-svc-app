import json
import httpx
from fastapi import HTTPException, status
from models.transaction import TransactionStatus
from decimal import Decimal
from typing import Optional
import logging

class TransactionService:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)
        self.DAPR_STATE_URL = "http://localhost:3510/v1.0/state/statestore"

    async def add_transaction(self, account_id, transaction):
        account_key = f"account:{account_id}"
        
        current_transactions = await self.get_transactions(account_id)
        
        current_transactions.append(transaction)
        
        data = [{
            "key": account_key,
            "value": current_transactions
        }]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.DAPR_STATE_URL, data=json.dumps(data))
        
        if response.status_code == 204:
            self.logger.info(f"Transaction added to account {account_id} successfully.")
        else:
            self.logger.error(f"Failed to add transaction: {response.status_code}")

    async def get_transactions(self, account_id):
        account_key = f"account:{account_id}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.DAPR_STATE_URL}/{account_key}")
        
        if response.status_code == 200:
            transactions = response.json()
            print(transactions)
            return transactions if transactions else []
        else:
            self.logger.error(f"Failed to retrieve transactions: {response.status_code}")
            return []

    async def get_account(self, account_id: str):
        ACCOUNT_SERVICE_URL = "http://localhost:3520/v1.0/invoke/accounting-service/method/account"
        url = f"{ACCOUNT_SERVICE_URL}/{account_id}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                try:
                    return response.json()  
                except ValueError:
                    raise HTTPException(status_code=500, detail="Invalid JSON response from account service")
            else:
                raise HTTPException(status_code=response.status_code, detail="Account not found")
    
    async def update_account(self, account_id: str, account_data: dict):
        pubsub_URL = "http://localhost:3520/v1.0/publish/pubsub/updateAccount"
        
        async with httpx.AsyncClient() as client:
            response = await client.put(pubsub_URL, json=account_data)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Account not found")
            elif response.status_code != 204:
                raise HTTPException(status_code=response.status_code, detail="Failed to update account")
    
    async def create_transaction_record(self, account_id: str, amount: Decimal, operation: str, transaction_type: str, status: TransactionStatus, session: Optional[any] = None):
        transaction_doc = {
            "from_account": account_id,
            "amount": amount,
            "operation": operation,
            "transaction_type": transaction_type,
            "status": status, 
            "timestamp": {"$currentDate": {"timestamp": True}},
        }
        return transaction_doc

    async def update_account_balance(self, account_id: str, amount: Decimal, operation: str, transaction_type: str, session: Optional[any] = None):
        account = await self.get_account(account_id)
        current_balance = account["balance"]
        
        # Calculate modifier based on operation (credit or debit)
        modifier = 1 if operation == "credit" else -1
        new_balance = current_balance + (amount * modifier)

        if new_balance < 0 and operation == "debit":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient funds in account ID: {account_id} for debit operation"
            )
        
        account["balance"] = new_balance
        await self.update_account(account_id, account)
        
        transaction_doc = await self.create_transaction_record(account_id, amount, operation, transaction_type, TransactionStatus.COMPLETED, session)
        
        await self.add_transaction(account_id, transaction_doc)

    async def create_transaction(self, transaction_doc):
        try:
            async with await self.db.client.start_session() as session:
                async with session.start_transaction():
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
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "debit",
                            "WITHDRAWAL",
                            session
                        )
                    
                    elif transaction_doc["transaction_type"] == "DEPOSIT":
                        await self.update_account_balance(
                            transaction_doc["from_account"],
                            transaction_doc["amount"],
                            "credit",
                            "DEPOSIT",
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