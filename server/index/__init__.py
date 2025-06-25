import numpy as np
from database.mongodb import MongoDB
from index.faiss_index import FaissIndex
from config import FAISS_INDEX_PATH

def build_faiss_index_from_postgres(database, index_path=FAISS_INDEX_PATH, dim=384):
    db = MongoDB()
    faiss_index = FaissIndex(dim=dim, index_path=index_path)

    # Fetch all caption_id and embedding from DB
    db.cursor.execute("SELECT caption_id, embedding FROM caption_table WHERE embedding IS NOT NULL;")
    results = db.cursor.fetchall()

    if not results:
        print("No embeddings found in database.")
        return

    ids = []
    vectors = []

    for row in results:
        caption_id, embedding = row
        if embedding:
            ids.append(caption_id)
            vectors.append(np.array(embedding, dtype=np.float32))

    embeddings_np = np.vstack(vectors)
    ids_np = np.array(ids)

    print(f"Building FAISS index with {len(ids)} vectors...")
    faiss_index.build(embeddings_np, ids_np)
    faiss_index.save()
    print(f"FAISS index saved to {index_path}")
    

def sync_faiss_index_from_postgres(db_config, index_path=FAISS_INDEX_PATH, dim=384):
    faiss_index = FaissIndex(dim=dim, index_path=index_path)
    faiss_index.load()

    db = DBManager(**db_config)

    # Fetch unsynced captions
    db.cursor.execute("SELECT caption_id, embedding FROM caption_table WHERE embedding IS NOT NULL AND faiss_synced = FALSE;")
    rows = db.cursor.fetchall()

    if not rows:
        print("No new captions to sync.")
        return

    ids = []
    vectors = []

    for caption_id, embedding in rows:
        ids.append(caption_id)
        vectors.append(np.array(embedding, dtype=np.float32))

    ids_np = np.array(ids)
    vectors_np = np.vstack(vectors)

    print(f"Syncing {len(ids)} new captions into FAISS...")
    faiss_index.index.add_with_ids(vectors_np, ids_np)
    faiss_index.save()

    # Mark these as synced in DB
    db.mark_captions_as_synced(ids)
    print("Database updated with faiss_synced = TRUE")
