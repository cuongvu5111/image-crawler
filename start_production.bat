@echo off
echo ========================================
echo   Django Image Crawler - Production
echo ========================================

REM Chuyen ve thu muc project
cd /d "%~dp0"

echo.
echo Thu muc: %CD%
echo.

REM Kich hoat virtual environment neu co
if exist "venv\Scripts\activate.bat" (
    echo Kich hoat virtual environment...
    call venv\Scripts\activate.bat
)

REM Set production environment (su dung SQLite thay vi PostgreSQL)
REM set DJANGO_SETTINGS_MODULE=DjangoProject.settings_production
set DEBUG=False

echo.
echo [1/4] Kiem tra Python va dependencies...
py --version
if %errorlevel% neq 0 (
    echo Loi: Python khong duoc tim thay!
    pause
    exit /b 1
)

echo.
echo [2/4] Chay database migrations...
py manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo Loi khi chay migrations!
    pause
    exit /b 1
)

echo.
echo [3/4] Collect static files...
py manage.py collectstatic --noinput --clear
if %errorlevel% neq 0 (
    echo Canh bao: Khong the collect static files
)

echo.
echo [4/4] Khoi dong production server...
echo.
echo ========================================
echo   Production Server URLs:
echo   Local:    http://127.0.0.1:8008
echo   Network:  http://0.0.0.0:8008
echo
echo   Workers: 4
echo   Nhan Ctrl+C de dung server
echo ========================================
echo.

REM Khoi dong voi Django development server tren Windows (Gunicorn khong ho tro Windows)
py manage.py runserver 0.0.0.0:8008

echo.
echo Production server da dung.
echo.
pause
