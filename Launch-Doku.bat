@echo off
setlocal
echo ==========================================
echo       Wo ist meine Doku - Launcher
echo ==========================================
echo.

if not exist .venv (
    echo [ERROR] Virtual environment not found. 
    echo Please run 'install.bat' first.
    pause
    exit /b 1
)

echo [1/2] Activating environment...
call .venv\Scripts\activate

echo [2/2] Starting Discovery Dashboard...
echo.
echo * Tip: Browser will open automatically.
echo * Tip: To stop the app, close this window.
echo.

:: Run streamlit
streamlit run src/ui/app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application crashed. 
    echo Try running 'install.bat' again to fix dependencies.
    pause
)
