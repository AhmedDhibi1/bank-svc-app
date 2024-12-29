from fastapi import FastAPI
from core.config import settings
from db.mongodb import db
from api.endpoints import transaction

app = FastAPI()

# Include routes for transactions and account validations
app.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])
app.include_router(account.router, prefix="/accounts", tags=["Accounts"])
