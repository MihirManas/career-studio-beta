@echo off
echo ==========================================
echo Starting Career Studio Backend...
echo ==========================================

if not exist venv (
    echo Creating Virtual Environment...
    python -m venv venv
)

echo Activating Virtual Environment...
call venv\Scripts\activate.bat

echo Installing Requirements...
pip install -r requirements.txt

echo.
echo Starting FastAPI Server...
echo The UI will be available at: http://127.0.0.1:8000/ui
echo.

uvicorn main:app --reload
