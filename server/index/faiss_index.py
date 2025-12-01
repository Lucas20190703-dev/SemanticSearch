# server/app/index/faiss_index.py

import faiss
import numpy as np
import os
import hashlib
from config import FAISS_INDEX_PATH, EMBEDDING_DIM, FAISS_IVF_INDEX_PATH

class FaissIndex:
    def __init__(self, dim: int = EMBEDDING_DIM, index_path=FAISS_INDEX_PATH):
        self.dim = dim
        self.index_path = str(index_path)

        # Load existing IVF index if available
        if os.path.exists(FAISS_IVF_INDEX_PATH):
            self.index = faiss.read_index(str(FAISS_IVF_INDEX_PATH))
        elif os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            # Start with flat inner product index
            self.index = faiss.IndexIDMap(faiss.IndexFlatIP(self.dim))

    # -----------------------------
    # Normalize vectors for inner product similarity
    # -----------------------------
    def normalize(self, vectors: np.ndarray) -> np.ndarray:
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    # -----------------------------
    # Build index from numpy arrays
    # -----------------------------
    def build(self, embeddings: np.ndarray, ids: np.ndarray):
        embeddings = self.normalize(embeddings)
        self.index.add_with_ids(embeddings.astype("float32"), ids.astype("int64"))

    # -----------------------------
    # Save/load index
    # -----------------------------
    def save(self):
        faiss.write_index(self.index, self.index_path)

    def load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

    # -----------------------------
    # Search
    # -----------------------------
    def search(self, query_vector: np.ndarray, k=5):
        if hasattr(self.index, 'nprobe'):
            self.index.nprobe = 10
        query_vector = self.normalize(query_vector.astype("float32").reshape(1, -1))
        scores, indices = self.index.search(query_vector, k)
        return indices[0], scores[0]

    # -----------------------------
    # Insert new vectors
    # -----------------------------
    def insert(self, ids: list, embeddings: list):
        ids_np = np.array(ids, dtype=np.int64)
        vectors_np = self.normalize(np.vstack(embeddings).astype("float32"))
        self.index.add_with_ids(vectors_np, ids_np)
        self.promote_index_to_ivf()

    # -----------------------------
    # Promote to IVF for large datasets
    # -----------------------------
    def promote_index_to_ivf(self, threshold: int = 10000, nlist: int = 100):
        if self.index.ntotal >= threshold and isinstance(self.index.index, faiss.IndexFlatIP):
            print("Promoting FAISS index to IVF...")
            vectors = [self.index.reconstruct(i) for i in range(self.index.ntotal)]
            vectors_np = np.array(vectors, dtype=np.float32)

            quantizer = faiss.IndexFlatIP(self.dim)
            ivf_index = faiss.IndexIVFFlat(quantizer, self.dim, nlist, faiss.METRIC_INNER_PRODUCT)
            ivf_index.train(vectors_np)
            ivf_index.add(vectors_np)

            self.index = faiss.IndexIDMap(ivf_index)
            faiss.write_index(self.index, FAISS_IVF_INDEX_PATH)
            print("FAISS index promoted and saved.")

    # -----------------------------
    # Convert ObjectId to int64 for FAISS ID
    # -----------------------------
    def hash_objectid_to_int64(self, oid):
        h = hashlib.sha1(str(oid).encode("utf-8")).digest()
        return int.from_bytes(h[:8], byteorder='big', signed=True)

    # -----------------------------
    # Get basic index info
    # -----------------------------
    def info(self):
        return {
            "index_type": type(self.index).__name__,
            "total_vectors": self.index.ntotal,
            "dimension": self.dim
        }
