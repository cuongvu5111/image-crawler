@echo off
echo ========================================
echo   Django Image Crawler - Service Mode
echo ========================================

cd /d "%~dp0"
echo Thu muc: %CD%

REM Kich hoat virtual environment
if exist "venv\Scripts\activate.bat" (
    echo Kich hoat virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Khong tim thay virtual environment!
    exit /b 1
)

REM Set environment
set DEBUG=False

echo.
echo [1/4] Kiem tra Python...
python --version
if %errorlevel% neq 0 (
    echo Loi: Python khong hoat dong!
    exit /b 1
)

echo.
echo [2/4] Chay migrations...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo Loi khi chay migrations!
    exit /b 1
)

echo.
echo [3/4] Collect static files...
python manage.py collectstatic --noinput --clear
if %errorlevel% neq 0 (
    echo Canh bao: Khong the collect static files
)

echo.
echo [4/4] Khoi dong server...
echo.
echo ========================================
echo   Server URLs:
echo   Local:    http://127.0.0.1:8008
echo   Network:  http://0.0.0.0:8008
echo ========================================
echo.

python manage.py runserver 0.0.0.0:8008
