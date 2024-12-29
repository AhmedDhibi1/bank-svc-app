from fastapi import FastAPI
from core.config import settings
from db.mongodb import db
from api.endpoints import transaction
from dapr.clients import DaprClient

app = FastAPI(title="Banking Transaction Service")

# Initialize Dapr client
@app.on_event("startup")
async def startup_db_client():
    # Connect to the database
    await db.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    # Disconnect from the database
    await db.disconnect()

# Include transaction router
app.include_router(
    transaction.router,
    prefix=f"{settings.API_V1_STR}/transactions",
    tags=["transactions"]
)