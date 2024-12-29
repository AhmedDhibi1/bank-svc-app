from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime

def insert_transaction(transaction_data: dict, collection: Collection):
    transaction_data["timestamp"] = datetime.now()
    result = collection.insert_one(transaction_data)
    return result.inserted_id

def get_transaction_by_id(transaction_id: str, collection: Collection):
    return collection.find_one({"_id": ObjectId(transaction_id)})
