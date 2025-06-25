
import sys, os, datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from index.faiss_index import FaissIndex
from database.mongodb import MongoDB
from config import EMBEDDING_DIM, FAISS_INDEX_PATH, TSDAE_MODEL_DIR, TOP_K
import numpy as np
from sentence_transformers import SentenceTransformer

class HybridSearchEngine:
    def __init__(self):
        self.database = MongoDB()
        self.faiss_index = FaissIndex(dim=EMBEDDING_DIM, index_path=FAISS_INDEX_PATH)
        self.model = SentenceTransformer(TSDAE_MODEL_DIR, device="cpu")
        
        if os.path.exists(FAISS_INDEX_PATH):
            self.sync_index()
        else:
            self.rebuild_index()       

    def get_database(self):
        return self.database
    
    def get_faiss_index(self):
        return self.faiss_index
    
    def get_status_of_faiss_index(self):
        return {
            "index_type": type(self.faiss_index.index).__name__,
            "total_vectors": self.faiss_index.index.ntotal,
            "dimension": self.faiss_index.dim
        }
        
    def sync_index(self):
        query = {
            "embedding": {"$exists": True, "$ne": None},
            "faiss_id": None
        }
        rows = self.database.find(query)

        if not rows:
            print("No new captions to sync.")
            return

        ids, vectors, object_ids = [], [], []
        for row in rows:
            _id = row["_id"]
            faiss_id = self.faiss_index.hash_objectid_to_int64(_id)
            ids.append(faiss_id)
            vectors.append(np.array(row["embedding"], dtype=np.float32))
            object_ids.append(_id)

        self.faiss_index.insert(ids, vectors)
        self.faiss_index.save()
        
        for _id, faiss_id in zip(object_ids, ids):
            self.database.update_one(
                { "_id": _id },
                { "$set": {"faiss_id": str(faiss_id) }}
            )
        
        print(f"Synced {len(ids)} embeddings to FAISS and updated DB.")
        self.faiss_index.promote_index_to_ivf()
        
    def rebuild_index(self):
        query = { "embedding": None }
        results = self.database.find({})

        vectors, ids, object_ids = [], [], []

        for row in results:
            obj_id = row["_id"]
            object_ids.append(obj_id)
            
            embedding = row["embedding"]
            
            ids.append(self.faiss_index.hash_objectid_to_int64(obj_id))
            
            if not embedding:
                caption = row["caption"]
                embedding = self.model.encode(caption).reshape(1, -1).tolist()
            vectors.append(embedding)

        if not vectors:
            print("No embeddings found.")
            return

        embeddings_np = np.vstack(vectors)
        ids_np = np.array(ids, dtype=np.int64)

        self.faiss_index.build(embeddings_np, ids_np)
        self.faiss_index.save()
        
        # update database
        for _id, faiss_id in zip(object_ids, ids):
            self.database.update_one(
                { "_id": _id },
                { "$set": {"faiss_id": str(faiss_id) }}
            )
        
        
        print(f"FAISS index built with {len(ids)} vectors.")
        self.faiss_index.promote_index_to_ivf()
        
    def search(self, 
               content: str = None, 
               top_k: int = TOP_K,
               similarity: float = 0.1,
               keywords: list = None, 
               categories: list = None, 
               created_after: str = None,
               created_before: str = None,
               name_contains: str = None,
               creator: str = None,
               writer: str = None):
        """
        Perform hybrid semantic + metadata filtering:
        - FAISS semantic
        - keywords match (any)
        - categories match (any)
        - time range filter
        - name regex filter (e.g. caption contains...)
        - top_k results
        """
        
        # Step 1: Vector search
        if content is not None:
            query = self.model.encode(content, convert_to_numpy=True)
            
            ids, scores = self.faiss_index.search(query.reshape(1, -1), k=top_k * 3)
            
            faiss_id_score_map = {str(id): float(score) for id, score in zip(ids, scores)}

            id_list = list(faiss_id_score_map.keys())
        else:
            id_list = None
        
        # Step 2: metadata filtering
        results = self.database.find_by_faiss_ids(
            ids = id_list, 
            keywords=keywords, 
            categories=categories, 
            created_after=created_after, 
            created_before=created_before, 
            name_contains=name_contains,
            creator=creator,
            writer=writer)
        
        for doc in results:
            doc["_id"] = str(doc["_id"])
            doc["created_at"] = doc["created_at"].isoformat()

        fields_remain = ["name", "creator", "path", "created_at", "caption", "writer", "faiss_id"]
        results = [
            {k: v for k, v in item.items() if k in fields_remain}
            for item in results
        ]
        if content is None:
            return results[:top_k]
        
        # Step 3: score filtering
        final = []
        for doc in results:
            f_id = doc["faiss_id"]
            
            score = faiss_id_score_map.get(f_id, 0.0)
            if similarity is not None and score < similarity:
                continue
            doc["score"] = score
            final.append(doc)
            
        # Step 4: Return top_k sorted by score
        final.sort(key=lambda x: x["score"], reverse=True)
        
        return final[:top_k]   
    