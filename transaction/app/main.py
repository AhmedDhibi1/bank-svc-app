from fastapi import FastAPI
from dapr.clients import DaprClient
from app.core.config import settings
from app.db.mongodb import db
from app.api.endpoints import transaction

app = FastAPI(title="Banking Transaction Service")

# Initialize Dapr client
dapr_client = DaprClient()

@app.on_event("startup")
async def startup_db_client():
    await db.connect()
    # This is where Dapr client can be used in the future for service invocation or other tasks.
    print("Dapr client initialized.")

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.disconnect()
    # Clean up or close the Dapr client when shutting down
    dapr_client.close()
    print("Dapr client closed.")

app.include_router(
    transaction.router,
    prefix=f"{settings.API_V1_STR}/transactions",
    tags=["transactions"]
)