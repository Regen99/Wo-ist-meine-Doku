@echo off
setlocal
echo ==========================================
echo   Wo ist meine Doku - Setup (CPU Mode)
echo ==========================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

:: 2. Create VENV if not exists
if not exist .venv (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
) else (
    echo [SKIP] Virtual environment already exists.
)

:: 3. Install Dependencies
echo [2/3] Installing CPU-optimized libraries (this may take a few minutes)...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-cpu.txt

:: 4. Finalize
if not exist data\raw mkdir data\raw
echo.
echo [3/3] Setup Complete! 
echo.
echo You can now use 'Launch-Doku.bat' to start the app.
pause
