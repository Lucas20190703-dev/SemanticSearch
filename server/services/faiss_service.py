# app/services/faiss_service.py

import os
import numpy as np
from sentence_transformers import SentenceTransformer

from index.faiss_index import FaissIndex
from services.mongodb_service import MongoDB  # your mongodb.py wrapper
from config import EMBEDDING_DIM, FAISS_INDEX_PATH, FAISS_IVF_INDEX_PATH, TSDAE_MODEL_DIR, TOP_K

class HybridSearchEngine:
    """
    Hybrid Search Engine combining:
    - FAISS vector search
    - MongoDB metadata filtering
    """
    def __init__(self, device="cpu"):
        self.database = MongoDB()

        self.faiss_index = FaissIndex(dim=EMBEDDING_DIM, index_path=FAISS_INDEX_PATH)
        self.model = SentenceTransformer(str(TSDAE_MODEL_DIR), device=device)

        if os.path.exists(FAISS_INDEX_PATH) or os.path.exists(FAISS_IVF_INDEX_PATH):
            self.sync_index()
        else:
            self.rebuild_index()

    # -----------------------------
    # Sync new embeddings to FAISS
    # -----------------------------
    def sync_index(self):
        query = {"embedding": {"$exists": True, "$ne": None}, "faiss_id": None}
        rows = self.database.find(query)

        if not rows:
            print("No new embeddings to sync.")
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

        # Update MongoDB
        for _id, faiss_id in zip(object_ids, ids):
            self.database.update_one({"_id": _id}, {"$set": {"faiss_id": str(faiss_id)}})

        print(f"Synced {len(ids)} embeddings to FAISS.")
        self.faiss_index.promote_index_to_ivf()

    # -----------------------------
    # Rebuild FAISS from scratch
    # -----------------------------
    def rebuild_index(self):
        results = self.database.fetch_all_documents()

        if not results:
            print("No embeddings found in DB.")
            return

        vectors, ids, object_ids = [], [], []

        for row in results:
            obj_id = row["_id"]
            embedding = row.get("embedding")

            # Compute embedding if missing
            if embedding is None and row.get("caption"):
                embedding = self.model.encode(row["caption"]).reshape(1, -1).tolist()

            if embedding is None:
                continue

            ids.append(self.faiss_index.hash_objectid_to_int64(obj_id))
            vectors.append(embedding)
            object_ids.append(obj_id)

        embeddings_np = np.vstack(vectors)
        ids_np = np.array(ids, dtype=np.int64)

        self.faiss_index.build(embeddings_np, ids_np)
        self.faiss_index.save()

        # Update DB
        for _id, faiss_id in zip(object_ids, ids):
            self.database.update_one({"_id": _id}, {"$set": {"faiss_id": str(faiss_id)}})

        print(f"FAISS index rebuilt with {len(ids)} vectors.")
        self.faiss_index.promote_index_to_ivf()

    # -----------------------------
    # Hybrid Search
    # -----------------------------
    def search(self, content=None, top_k=TOP_K, similarity=0.1,
            keywords=None, categories=None, created_after=None, created_before=None,
            name_contains=None, creator=None, writer=None):

        # Step 1: Vector search only if content exists
        if content:
            query_vec = self.model.encode(content, convert_to_numpy=True)
            ids, scores = self.faiss_index.search(query_vec.reshape(1, -1), k=top_k * 3)

            #faiss_map = {str(id_): float(score) for id_, score in zip(ids[0], scores[0])}
            faiss_map = {str(id_): float(score) for id_, score in zip(ids, scores)}
            id_list = list(faiss_map.keys())
        else:
            id_list = None          # means "no vector filter"
            faiss_map = {}

        # Step 2: Metadata search
        results = self.database.find_by_faiss_ids(
            ids=id_list,
            keywords=keywords,
            categories=categories,
            created_after=created_after,
            created_before=created_before,
            name_contains=name_contains,
            creator=creator,
            writer=writer
        )

        fields = ["name", "creator", "path", "created_at", "caption", "writer", "faiss_id"]
        final_results = []

        for doc in results:
            doc["_id"] = str(doc["_id"])
            doc["created_at"] = doc["created_at"].isoformat()

            # Only compute score if FAISS was used
            if content:
                score = faiss_map.get(doc["faiss_id"], 0.0)
                if score < similarity:
                    continue
                doc["score"] = score
                final_results.append({k: doc.get(k) for k in fields + ["score"]})
            else:
                # Pure metadata mode → no scores
                final_results.append({k: doc.get(k) for k in fields})

        # Sort only when scores exist
        if content:
            final_results.sort(key=lambda x: x["score"], reverse=True)

        return final_results[:top_k]

