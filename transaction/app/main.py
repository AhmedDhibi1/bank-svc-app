import json
from charset_normalizer import from_fp
from fastapi import FastAPI
from core.config import settings
from db.mongodb import db
from api.endpoints import transaction
<<<<<<< HEAD
from dapr.clients import DaprClient

app = FastAPI(title="Banking Transaction Service")

# Initialize Dapr client
=======
from dapr.ext.fastapi import DaprApp

app = FastAPI(title="Banking Transaction Service")


>>>>>>> 106ab3190ee04cf6c8a7d2a89e202bba90b10530
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


