import json
from charset_normalizer import from_fp
from fastapi import FastAPI
from core.config import settings
from db.mongodb import db
from api.endpoints import transaction
from dapr.ext.fastapi import DaprApp

app = FastAPI(title="Banking Transaction Service")


@app.on_event("startup")
async def startup_db_client():
    await db.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await db.disconnect()

app.include_router(
    transaction.router,
    prefix=f"{settings.API_V1_STR}/transactions",
    tags=["transactions"]
)


