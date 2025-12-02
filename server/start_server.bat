@echo off
setlocal

REM Set PYTHONPATH to current directory
set PYTHONPATH=.

REM Start API server
start cmd /k "uvicorn main:app --reload --port 3000"

echo Backend Server started.
