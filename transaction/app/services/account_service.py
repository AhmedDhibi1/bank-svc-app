import httpx
from app.config import settings

async def validate_account(account_id: str, amount: float, transaction_type: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.ACCOUNT_SERVICE_URL}/{account_id}")
        if response.status_code == 200:
            account_data = response.json()
            current_balance = account_data.get("balance", 0)
            if transaction_type == "debit" and current_balance < amount:
                return False
            return True
        return False

async def update_account_balance(account_id: str, amount: float, transaction_type: str) -> bool:
    async with httpx.AsyncClient() as client:
        if transaction_type == "debit":
            response = await client.put(f"{settings.ACCOUNT_SERVICE_URL}/{account_id}/debit", json={"amount": amount})
        elif transaction_type == "credit":
            response = await client.put(f"{settings.ACCOUNT_SERVICE_URL}/{account_id}/credit", json={"amount": amount})
        
        return response.status_code == 200
