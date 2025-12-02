# server/app/api/routes.py

import io
import os
import csv
import mimetypes
from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, Header, Query, Request, Depends
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional

from models.schema import InsertCaptionRequest, SearchRequest
from services.faiss_service import HybridSearchEngine
from config import API_TOKEN, FILE_ROOT_DIR
from utils.file_system import get_directory_structure, get_files_from_directory
import services.expansionnetv2_module as Module

# Initialize router
router = APIRouter()

# --------------------------
# Auth dependency
# --------------------------
def verify_token(token: str = Header(...)):
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")

# --------------------------
# Initialize hybrid search engine
# --------------------------
search_engine = HybridSearchEngine()

# --------------------------
# API Endpoints
# --------------------------

@router.post("/api/search")
def semantic_search(req: SearchRequest):
    """
    Perform hybrid semantic + metadata search
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
            name_contains=req.name_contains,
            creator=req.creator,
            writer=req.writer
        )

        # CSV OUTPUT
        if req.format == "csv" and results:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
            output.seek(0)
            return StreamingResponse(
                output,
                media_type="text/csv",
                headers={
                    "Content-Disposition": "attachment; filename=search_results.csv"
                }
            )

        # JSON OUTPUT
        return results   # FastAPI will automatically JSON-serialize

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/caption")
def get_caption(file: str):
    print(f"Getting caption for: {file}")    
    _, caption = Module.get_caption(file)
    return {"caption": caption}



# --------------------------
# FAISS Management
# --------------------------
@router.post("/api/faiss/sync")
def sync_faiss(_: str = Depends(verify_token)):
    """
    Sync unsynced embeddings from MongoDB to FAISS
    """
    try:
        search_engine.sync_index()
        return {"status": "success", "message": "FAISS index synced"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/faiss/rebuild")
def rebuild_faiss(_: str = Depends(verify_token)):
    """
    Rebuild FAISS index from all embeddings
    """
    try:
        search_engine.rebuild_index()
        return {"status": "success", "message": "FAISS index rebuilt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/faiss/status")
def faiss_status():
    """
    Returns FAISS index info: size, type, dimension
    """
    try:
        return search_engine.get_status_of_faiss_index()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------
# Caption Insertion
# --------------------------
@router.post("/api/caption/insert")
def insert_caption(req: InsertCaptionRequest, _: str = Depends(verify_token)):
    """
    Insert a new caption + optional metadata
    """
    try:
        inserted_id = search_engine.get_database().insert(
            path=req.path,
            caption=req.caption,
            writer=req.writer,
            creator=req.creator
        )
        if not inserted_id:
            raise HTTPException(status_code=400, detail="Failed to insert caption")
        return {"status": "success", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------
# File System Endpoints
# --------------------------
@router.get("/api/directories")
def get_directories():
    return JSONResponse(get_directory_structure(FILE_ROOT_DIR))

@router.get("/api/files/{dir_path:path}")
def get_files(dir_path: str, offset: int = Query(0), limit: int = Query(-1)):
    # Build full path
    full_path = os.path.abspath(os.path.join(FILE_ROOT_DIR, dir_path))

    # Security check: prevent access outside FILE_ROOT_DIR
    if not full_path.startswith(os.path.abspath(FILE_ROOT_DIR)):
        raise HTTPException(status_code=403, detail="Access denied")

    # Get files
    files_list = get_files_from_directory(full_path, offset, limit)
    return files_list

@router.get("/api/download/{file_path:path}")
def download_file(file_path: str):
    full_path = os.path.join(FILE_ROOT_DIR, file_path)

    # Security check
    if not os.path.abspath(full_path).startswith(os.path.abspath(FILE_ROOT_DIR)):
        return JSONResponse(status_code=403, content={"error": "Access denied"})

    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})

    return FileResponse(full_path, filename=os.path.basename(full_path))

@router.get("/api/media/{file_path:path}")
def get_media(request: Request, file_path: str):
    decoded_path = unquote(file_path)
    full_path = os.path.join(FILE_ROOT_DIR, decoded_path)
    filetype, _ = mimetypes.guess_type(full_path)

    if not filetype:
        raise HTTPException(status_code=400, detail="Unknown file type")
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path, media_type=filetype)
