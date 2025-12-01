# server/app/main.py

"""
Main entry point for the semantic search API server.

Launch with:
    PYTHONPATH=. uvicorn app.main:app --reload

Author: Lucas
Date: 2025-06-05
"""

import sys, os
from pathlib import Path


sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from services.background_runner import BackgroundRunner
from services.expansionnetv2_module import init_expansionnetv2_model

# Import the router
from api.routes import router

# Config for file root directory
from config import FILE_ROOT_DIR, TSDAE_MODEL_DIR

app = FastAPI(
    title="Semantic Search API",
    description="FAISS + MongoDB hybrid search backend",
    version="1.0.0"
)

# Allow CORS (frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# load expansionnet model
init_expansionnetv2_model()

@app.on_event("startup")
async def startup_event():
    runner = BackgroundRunner(model_dir=TSDAE_MODEL_DIR, interval=30)
    asyncio.create_task(runner.run())

# Optional root path
@app.get("/")
def root():
    return {"message": "Semantic Search API is running"}

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
