"""
API Router for Semantic Search
------------------------------
Exposes REST API for performing semantic search via FAISS + SentenceTransformer.

- Loads encoder and FAISS index
- Accepts POST /search with query text and returns top-k relevant documents

Author: Lucas
Date: 2025-06-05
"""

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, HTTPException, Depends, Header, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import csv
import io

from search.hybrid_search import HybridSearchEngine

from file_system import *

# Create router
router = APIRouter()

# Auth token and middleware
API_TOKEN = "my-secret-token"

def verify_token(token: str = Header(...)):
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")


# Init hybrid engine
search_engine = HybridSearchEngine()

# Request/response models
class SearchRequest(BaseModel):
    content: str = None
    top_k: int = 5
    similarity: float = 0.1
    keywords: list = None
    categories: list = None
    created_after: str = None
    created_before: str = None
    name_contains: str = None
    format: Optional[str] = "json"  # json or csv

@router.post("/api/search")
async def semantic_search(req: SearchRequest):
    """
    POST /api/search
    Perform semantic search using FAISS + MongoDB metadata
    """
    try:
        results = search_engine.search(
            content=req.content, 
            top_k=req.top_k, 
            similarity=req.similarity,
            keywords=req.keywords,
            categories=req.categories,
            created_after=req.created_after,
            created_before=req.created_before,
            name_contains=req.name_contains)

        if req.format == "csv":
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
            output.seek(0)
            return StreamingResponse(output, media_type="text/csv", headers={
                "Content-Disposition": "attachment; filename=search_results.csv"
            })

        return JSONResponse(content=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/faiss/sync")
def sync_faiss(_: str = Depends(verify_token)):
    """
    POST /api/faiss/sync
    Add new unsynced caption embeddings to FAISS index and mark them as synced
    """
    try:
        search_engine.sync_index()
        return {"status": "success", "message": "FAISS index synced"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/faiss/rebuild")
def rebuild_faiss(_: str = Depends(verify_token)):
    """
    POST /faiss/rebuild
    Rebuild the FAISS index from all caption embeddings and mark as synced
    """
    try:
        search_engine.rebuild_index()
        return {"status": "success", "message": "FAISS index rebuilt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/faiss/status")
def faiss_status():
    """
    GET /faiss/status
    Returns FAISS index info: size, type, dimension
    """
    try:
        return search_engine.get_status_of_faiss_index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/caption/insert")
def insert_cation(path: str, caption: str, writer: str=None, _: str = Depends(verify_token)):
    """
    POST /caption/insert
    Args:
        path (str): file path
        caption (str): caption for the file
        owner: the writer of caption
        _ (str, optional): _description_. Defaults to Depends(verify_token).
    """
    
    
# File system 

@router.get("/api/directories")
def get_directories():
    return JSONResponse(get_directory_structure(ROOT_DIR))

@router.get("/api/files/{dir_path:path}")
def get_files(dir_path: str, offset: int = Query(0), limit: int = Query(20)):
    path = (ROOT_DIR / dir_path).resolve()
    return JSONResponse(get_files_from_directory(path, offset, limit))

@router.get("/api/download/{file_path:path}")
def download_file(file_path: str):
    full_path = (ROOT_DIR / file_path).resolve()

    # Security check
    if not str(full_path).startswith(str(ROOT_DIR)):
        return JSONResponse(status_code=403, content={"error": "Access denied"})

    if not full_path.exists() or not full_path.is_file():
        return JSONResponse(status_code=404, content={"error": "File not found"})

    return FileResponse(full_path, filename=full_path.name)


@router.get("/api/media/{file_path:path}")
def get_media(request: Request, file_path: str):
    # Decode and normalize path
    decoded_path = unquote(file_path).replace("/", os.sep)
    
    filetype, _ = mimetypes.guess_type(decoded_path)
    if not filetype:
        raise HTTPException(status_code=500, detail="Unknown support file type.")
    
    print("Filetype:", filetype, decoded_path)
    if filetype.startswith("image/"):
        if not os.path.exists(decoded_path):
            raise HTTPException(status_code=404, detail="Image not found")
        return FileResponse(decoded_path, media_type="image/jpeg")
    elif filetype.startswith("video/"):
        return get_video_stream(request, file_path)


def get_video_stream(request: Request, file_path: str):
    range_header = request.headers.get('range')
    file_size = os.path.getsize(file_path)

    start = 0
    end = file_size - 1

    if range_header:
        range_val = range_header.strip().split('=')[-1]
        start_end = range_val.split('-')
        start = int(start_end[0])
        if len(start_end) > 1 and start_end[1]:
            end = int(start_end[1])

    chunk_size = (end - start) + 1

    def iter_file():
        with open(file_path, "rb") as f:
            f.seek(start)
            yield f.read(chunk_size)

    return StreamingResponse(
        iter_file(),
        media_type="video/mp4",
        status_code=206,
        headers={
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(chunk_size),
        }
    )