from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime
from config import MONGO_DB_NAME, MONGO_DB_PORT, MONGO_DB_HOST

import os
from bson import ObjectId

class MongoDB:
    def __init__(self, host=MONGO_DB_HOST, port = MONGO_DB_PORT, db_name=MONGO_DB_NAME):
        self.client = MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        self.documents = self.db["caption_table"]

        self.documents.create_index({"keywords": 1})
        self.documents.create_index({"categories": 1})
        self.documents.create_index({"writer": 1})
        self.documents.create_index({"creator": 1})
        self.documents.create_index({"created_at": -1})

    def insert(self, **kwargs) -> Optional[str]:
        path = kwargs.get("path", None)
        creator = kwargs.get("creator", None)
        caption = kwargs.get("caption", None)
        writer = kwargs.get("writer", None)
        categories = kwargs.get("categories", None)
        keywords = kwargs.get("keywords", None)
        embedding = kwargs.get("embedding", None)
        faiss_id = kwargs.get("faiss_id", None)

        if path is None:
            return None

        name = os.path.basename(path)

        if os.path.exists(path):
            status = os.stat(path)
            timenow = datetime.fromtimestamp(status.st_ctime)
        else:
            timenow = datetime.now()

        doc = {
            "name": name,
            "creator": creator,
            "path": path,
            "created_at": timenow,
            "caption": caption,
            "writer": writer,
            "categories": categories,
            "keywords": keywords,
            "embedding": embedding,
            "faiss_id": faiss_id
        }

        result = self.documents.insert_one(doc)
        return str(result.inserted_id)

    def find(self, query = None):
        return list(self.documents.find(query))

    def find_one(self, query):
        return self.documents.find_one(query)

    def update_many(self, filter_query, update_values):
        return self.documents.update_many(filter_query, update_values).modified_count

    def update_one(self, filter_query, update_values):
        return self.documents.update_one(filter_query, update_values).modified_count

    def remove(self, query) -> int:
        return self.documents.delete_many(query).deleted_count

    def fetch_all_documents(self):
        return list(self.documents.find({}))

    def find_by_ids(self, ids: List[str]=None, **kwargs):
        """
        Find captions by a list of IDs, plus optional filters via kwargs:
        - keywords: list of keyword
        - categories: list of category
        - created_after: ISO date string
        - created_before: ISO date string
        - name_contains: partial match on caption field
        - creator: file creator
        - writer: writer of caption
        """
        query = {}

        if ids:
            query["_id"] = {"$in": ids}

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
            if "created_after" in kwargs and kwargs["created_after"]:
                query["created_at"]["$gte"] = datetime.fromisoformat(kwargs["created_after"])
            if "created_before" in kwargs and kwargs["created_before"]:
                query["created_at"]["$lte"] = datetime.fromisoformat(kwargs["created_before"])

        if "name_contains" in kwargs and kwargs["name_contains"]:
            query["caption"] = {"$regex": kwargs["name_contains"], "$options": "i"}

        limit = int(kwargs.get("limit", 0))
        skip = int(kwargs.get("skip", 0))

        cursor = self.documents.find(query).skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)

    def find_by_faiss_ids(self, ids: List[str]=None, **kwargs):
        """
        Find captions by a list of faiss_ids, plus optional filters via kwargs:
        - keywords: list of keyword
        - categories: list of category
        - created_after: ISO date string
        - created_before: ISO date string
        - name_contains: partial match on caption field
        - creator: file creator
        - writer: writer of caption
        """
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
            # query["created_at"] = {}
            if "created_after" in kwargs and kwargs["created_after"]:
                query["created_at"]["$gte"] = datetime.fromisoformat(kwargs["created_after"])
            if "created_before" in kwargs and kwargs["created_before"]:
                query["created_at"]["$lte"] = datetime.fromisoformat(kwargs["created_before"])

        if "name_contains" in kwargs and kwargs["name_contains"]:
            query["caption"] = {"$regex": kwargs["name_contains"], "$options": "i"}

        limit = int(kwargs.get("limit", 0))
        skip = int(kwargs.get("skip", 0))

        
        
        cursor = self.documents.find(query).skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        return list(cursor)


    def clear(self):
        self.documents.delete_many({})        

    def close(self):
        self.client.close()

    def lookup(self):
        print(self.client.server_info())
        print(self.db.list_collection_names())
        print(self.db.command("collstats", "caption_table"))

        indexes = self.documents.index_information()
        for name, info in indexes.items():
            print(f"{name}: {info}")
