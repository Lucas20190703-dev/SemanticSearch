# server/app/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# -----------------------------
# Request Models
# -----------------------------

class SearchRequest(BaseModel):
    content: Optional[str] = None
    top_k: int = 30
    similarity: float = 0.1
    keywords: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    created_after: Optional[str] = None
    created_before: Optional[str] = None
    name_contains: Optional[str] = None
    creator: Optional[str] = None
    writer: Optional[str] = None
    format: Optional[str] = "json"  # "json" or "csv"

class InsertCaptionRequest(BaseModel):
    path: str
    caption: str
    writer: Optional[str] = None
    creator: Optional[str] = None
    keywords: Optional[List[str]] = None
    categories: Optional[List[str]] = None

# -----------------------------
# Response Models
# -----------------------------

class CaptionResponse(BaseModel):
    _id: str
    name: str
    path: str
    caption: Optional[str] = None
    creator: Optional[str] = None
    writer: Optional[str] = None
    categories: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    created_at: datetime
    faiss_id: Optional[str] = None
    score: Optional[float] = None

class FAISSStatusResponse(BaseModel):
    index_type: str
    total_vectors: int
    dimension: int
