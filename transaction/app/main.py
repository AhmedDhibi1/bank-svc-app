from fastapi import FastAPI
from app.routes import transaction, account

app = FastAPI()

# Include routes for transactions and account validations
app.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])
app.include_router(account.router, prefix="/accounts", tags=["Accounts"])
