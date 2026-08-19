@echo off
call venv\Scripts\activate
python -m uvicorn api.main:app --reload
pause
