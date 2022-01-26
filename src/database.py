from typing import (
    Any,
    Dict,
    List,
    Union
)
from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.client["social-media-api"]
        # self.collection = self.database[username]

    def collection_exists(self, collection: str) -> bool:
        collections = self.database.list_collection_names()
        return True if collection in collections else False

    def insert(
        self,
        collection: str,
        document: Dict[str, Any]
    ) -> bool:
        self.database[collection].insert_one(document)
        return True

    def read(
        self,
        collection: str,
        queries: List[Dict[Any, Any]] = [{}]
    ):
        if not self.collection_exists(collection):
            return False
        try:
            data = self.database[collection].find(*queries)
            return list(data)
        except:
            return False

    def update(
        self,
        collection: str,
        document: Dict[str, Any],
        updated_document: Dict[str, Any]
    ) -> bool:
        if not self.collection_exists(collection):
            return False
        self.database[collection].update_one(
            document,
            {"$set": updated_document},
            upsert = False
        )
        return True

    def delete(
        self,
        collection: str,
        document: Dict[str, Any]
    ) -> bool:
        if not self.collection_exists(collection):
            return False
        self.database[collection].delete_one(document)
        return True
