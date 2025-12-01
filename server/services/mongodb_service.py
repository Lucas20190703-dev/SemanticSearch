# server/app/services/mongodb_service.py

from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import os

from config import MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_NAME

class MongoDB:
    def __init__(self, host=MONGO_DB_HOST, port=MONGO_DB_PORT, db_name=MONGO_DB_NAME):
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.documents = self.db["caption_table"]

        # Create indexes
        self.documents.create_index({"keywords": 1})
        self.documents.create_index({"categories": 1})
        self.documents.create_index({"writer": 1})
        self.documents.create_index({"creator": 1})
        self.documents.create_index({"created_at": -1})

    # -----------------------------
    # Insert a document
    # -----------------------------
    def insert(self, **kwargs) -> Optional[str]:
        path = kwargs.get("path")
        if not path:
            return None

        doc = {
            "name": os.path.basename(path),
            "path": path,
            "caption": kwargs.get("caption"),
            "creator": kwargs.get("creator"),
            "writer": kwargs.get("writer"),
            "categories": kwargs.get("categories"),
            "keywords": kwargs.get("keywords"),
            "embedding": kwargs.get("embedding"),
            "faiss_id": kwargs.get("faiss_id"),
            "created_at": datetime.now()
        }

        result = self.documents.insert_one(doc)
        return str(result.inserted_id)

    # -----------------------------
    # Fetch all documents
    # -----------------------------
    def fetch_all_documents(self):
        return list(self.documents.find({}))

    # -----------------------------
    # General find
    # -----------------------------
    def find(self, query=None):
        if query is None:
            query = {}
        return list(self.documents.find(query))

    def find_one(self, query):
        return self.documents.find_one(query)

    def update_one(self, filter_query, update_values):
        return self.documents.update_one(filter_query, update_values).modified_count

    def update_many(self, filter_query, update_values):
        return self.documents.update_many(filter_query, update_values).modified_count

    def remove(self, query) -> int:
        return self.documents.delete_many(query).deleted_count

    # -----------------------------
    # Find by FAISS IDs + optional filters
    # -----------------------------
    def find_by_faiss_ids(self, ids: List[str] = None, **kwargs):
        query = {}
        if ids:
            query["faiss_id"] = {"$in": ids}

        if "keywords" in kwargs and kwargs["keywords"]:
            query["keywords"] = {"$in": kwargs["keywords"]}

        if "categories" in kwargs and kwargs["categories"]:
            query["categories"] = {"$in": kwargs["categories"]}

        if "writer" in kwargs and kwargs["writer"]:
            query["writer"] = kwargs["writer"]

        if "creator" in kwargs and kwargs["creator"]:
            query["creator"] = kwargs["creator"]

        if "created_after" in kwargs or "created_before" in kwargs:
            query["created_at"] = {}
            if kwargs.get("created_after"):
                query["created_at"]["$gte"] = datetime.fromisoformat(kwargs["created_after"])
            if kwargs.get("created_before"):
                query["created_at"]["$lte"] = datetime.fromisoformat(kwargs["created_before"])

        if "name_contains" in kwargs and kwargs["name_contains"]:
            query["caption"] = {"$regex": kwargs["name_contains"], "$options": "i"}

        limit = int(kwargs.get("limit", 0))
        skip = int(kwargs.get("skip", 0))

        cursor = self.documents.find(query).skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    # -----------------------------
    # Cleanup / Close connection
    # -----------------------------
    def clear(self):
        self.documents.delete_many({})

    def close(self):
        self.client.close()
