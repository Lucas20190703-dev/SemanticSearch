"""
Web frontend to interact with the Semantic Search API.
Launches a small FastAPI app with HTML form and renders search results.

Run:
    uvicorn web_client.main:app --reload

Author: Lucas
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="web_client/static"), name="static")

templates = Jinja2Templates(directory="web_client/templates")

API_URL = "http://localhost:3000/api/search"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request, "results": None})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...), top_k: int = Form(5)):
    try:
        response = requests.post(API_URL, json={"content": query, "top_k": top_k})
        
        results = response.json()
        print("Search results:", results)
    except Exception as e:
        results = [{"id": "Error", "text": str(e), "score": 0.0}]
    
    return templates.TemplateResponse("index.html", {"request": request, "results": results, "query": query})
