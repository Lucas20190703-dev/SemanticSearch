"""
Main entry point for the semantic search API server.

Launch with:
    PYTHONPATH=. uvicorn app.main:app --reload

Author: Lucas
Date: 2025-06-05
"""
import sys, os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import router

from app.file_system import ROOT_DIR

app = FastAPI(
    title="Semantic Search API",
    description="FAISS + PostgreSQL hybrid search backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"] for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Optional root path
@app.get("/")
def root():
    return {"message": "Semantic Search API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
