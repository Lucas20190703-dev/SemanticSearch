# Semantic Text Search Engine

This project implements an end-to-end semantic search system using unsupervised sentence embedding training (TSDAE), FAISS indexing, and a FastAPI server.

---

## 🔧 Project Structure

```
semantic_search_project/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api.py               # API routes for semantic search
├── search/
│   ├── search_engine.py     # Core semantic search logic
├── train/                   # Tokenizer, MLM, TSDAE training scripts
├── models/                  # Saved models, FAISS index
├── data/                    # Input corpus
├── README.md
```

---

## 🚀 API Endpoints

### Root
`GET /`

Returns a welcome message.

### Search
`POST /search/`

**Request:**
```json
{
  "query": "What is semantic search?",
  "top_k": 5
}
```

**Response:**
```json
{
  "results": [
    {"id": 12, "text": "Semantic search enables..."},
    ...
  ]
}
```

### Get Document by ID
`GET /document/{doc_id}`

**Response:**
```json
{
  "id": 12,
  "text": "Semantic search enables...",
  "embedding": [...]
}
```

---

## 🧪 How to Run the Server

1. Install dependencies:
```bash
pip install fastapi uvicorn psycopg2-binary
```

2. Run the server:
```bash
uvicorn app.main:app --reload
```

The server will be available at `http://localhost:8000`.

---

## 🧠 Model and DB

- TSDAE-based sentence embedding trained with your corpus.
- FAISS for vector indexing.
- PostgreSQL for large-scale corpus storage.
