@echo off
echo ========================================
echo   Django Image Crawler - Production Service
echo   (Khong can NSSM)
echo ========================================

REM Chuyen ve thu muc project
cd /d "%~dp0"

echo.
echo Thu muc: %CD%
echo.

REM Kiem tra quyen Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Canh bao: Khong chay voi quyen Administrator
    echo Ung dung van co the hoat dong binh thuong
    echo.
)

REM Kich hoat virtual environment neu co
if exist "venv\Scripts\activate.bat" (
    echo Kich hoat virtual environment...
    call venv\Scripts\activate.bat
)

REM Set production environment (su dung SQLite thay vi PostgreSQL)
REM set DJANGO_SETTINGS_MODULE=DjangoProject.settings_production
set DEBUG=False

echo [1/4] Kiem tra Python...
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
echo [4/4] Tao thu muc logs...
if not exist "logs" mkdir logs

echo.
echo ========================================
echo   Production Server dang khoi dong...
echo
echo   URL Local:    http://127.0.0.1:8008
echo   URL Network:  http://0.0.0.0:8008
echo
echo   Workers: 4
echo   Timeout: 120s
echo
echo   Logs: logs\production.log
echo   Nhan Ctrl+C de dung server
echo ========================================
echo.

REM Khoi dong voi Gunicorn va log tren port 8008
py -m gunicorn --bind 0.0.0.0:8008 --workers 4 --timeout 120 --max-requests 1000 --preload --access-logfile logs\access.log --error-logfile logs\error.log --log-level info DjangoProject.wsgi:application

echo.
echo Production server da dung.
echo Xem logs tai: logs\
echo.
pause
