import asyncio
import mimetypes
import os
from pathlib import Path
import threading
from config import FILE_ROOT_DIR, TSDAE_MODEL_DIR, FAISS_INDEX_PATH, EMBEDDING_DIM
from services.faiss_service import HybridSearchEngine, FaissIndex
from services.mongodb_service import MongoDB
from sentence_transformers import SentenceTransformer
import numpy as np

from services.expansionnetv2_module import get_caption
from api.routes import search_engine

class BackgroundRunner:
    def __init__(self, model_dir=TSDAE_MODEL_DIR, interval=30):
        self.model = SentenceTransformer(str(model_dir.resolve()))
        self.db = MongoDB()
        self.interval = interval  # seconds
        self.faiss_lock = threading.Lock()

    async def run(self):
        """
        Start the background runner loop.
        """
        while True:
            await self.scan_and_index()
            await asyncio.sleep(self.interval)

    async def scan_and_index(self):
        """
        Scan files under FILE_ROOT_DIR, generate embeddings,
        insert new files into MongoDB and FAISS index.
        """
        for root, dirs, files in os.walk(FILE_ROOT_DIR):
            for file in files:
                file_path = Path(root) / file

                # Skip hidden files
                if file.startswith("."):
                    continue

                # Skip if already indexed
                if self.db.find_one({"path": str(file_path)}):
                    continue
                
                mime_type, _ = mimetypes.guess_type(str(file_path))
                if mime_type is None or not (mime_type.startswith("image")):
                    continue

                _, caption = get_caption(str(file_path))

                # Generate embedding
                embedding = self.model.encode(caption).tolist()

                faiss_id = search_engine.faiss_index.hash_objectid_to_int64(str(file_path))

                # Insert into MongoDB
                inserted_id = self.db.insert(
                    path=str(file_path),
                    caption=caption,
                    faiss_id=faiss_id,
                )

                if not inserted_id:
                    continue

                # Insert into FAISS safely
                with self.faiss_lock:
                    search_engine.faiss_index.insert([faiss_id], [embedding])
                    search_engine.faiss_index.save()

                print(f"[BackgroundRunner] Indexed: {file_path} -> {inserted_id}")
