@echo off
echo Removing __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo Removing .pyc files...
del /s /q *.pyc

echo Cleanup complete.