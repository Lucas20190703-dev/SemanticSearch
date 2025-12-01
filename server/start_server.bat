@echo off
setlocal

REM Set PYTHONPATH to current directory
set PYTHONPATH=../.venv/Scripts

REM Start API server
start cmd /k "uvicorn app.main:app --reload --port 3000"

echo Backend Server started.
