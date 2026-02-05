@echo off
echo Hill Drive API - Diagnostic Tool
echo ==================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo [FAIL] Python not found
    goto :end
) else (
    echo [OK] Python found
)
echo.

echo Checking pip...
pip --version
if errorlevel 1 (
    echo [FAIL] pip not found
    goto :end
) else (
    echo [OK] pip found
)
echo.

echo Checking virtual environment...
if exist venv (
    echo [OK] venv folder exists
) else (
    echo [INFO] venv folder not found - will be created on first run
)
echo.

echo Checking .env file...
if exist .env (
    echo [OK] .env file exists
    echo Contents:
    type .env
) else (
    echo [INFO] .env file not found - will be created from .env.example
)
echo.

echo Checking template file...
if exist "inn sample.xlsx" (
    echo [OK] Template file found
) else (
    echo [FAIL] Template file 'inn sample.xlsx' not found!
)
echo.

echo Checking output directory...
if exist generated_invoices (
    echo [OK] Output directory exists
) else (
    echo [INFO] Output directory will be created
)
echo.

echo Checking Python modules...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [INFO] fastapi not installed - run quick_start.bat to install
) else (
    echo [OK] fastapi installed
)

python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo [INFO] uvicorn not installed - run quick_start.bat to install
) else (
    echo [OK] uvicorn installed
)

python -c "import openpyxl" 2>nul
if errorlevel 1 (
    echo [INFO] openpyxl not installed - run quick_start.bat to install
) else (
    echo [OK] openpyxl installed
)
echo.

echo Checking main files...
if exist main.py (
    echo [OK] main.py found
) else (
    echo [FAIL] main.py not found!
)

if exist config.py (
    echo [OK] config.py found
) else (
    echo [FAIL] config.py not found!
)

if exist requirements.txt (
    echo [OK] requirements.txt found
) else (
    echo [FAIL] requirements.txt not found!
)
echo.

echo ==================================
echo Diagnostic Complete
echo ==================================
echo.
echo Next steps:
echo 1. If any [FAIL] items, fix them first
echo 2. Run: quick_start.bat
echo 3. Or manually: python -m uvicorn main:app --reload
echo.

:end
pause
