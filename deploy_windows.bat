@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    Django Image Crawler Deployment
echo ========================================

REM Chuyển về thư mục chứa file bat
cd /d "%~dp0"

echo.
echo 📁 Thư mục hiện tại: %CD%
echo.

REM Function để hiển thị progress bar
call :show_progress 0 "Bắt đầu deployment..."

echo.
echo [1/6] 🔍 Kiểm tra Python...
call :show_progress 10 "Kiểm tra Python..."
py --version
if %errorlevel% neq 0 (
    echo.
    echo ❌ Lỗi: Python không được tìm thấy!
    echo 💡 Vui lòng cài đặt Python hoặc thêm vào PATH
    pause
    exit /b 1
)
echo ✅ Python OK!

echo.
echo [2/6] 📦 Cài đặt dependencies...
call :show_progress 25 "Đang cài đặt packages..."
py -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Lỗi khi cài đặt dependencies!
    pause
    exit /b 1
)
echo ✅ Dependencies đã cài đặt!

echo.
echo [2/6] Collect static files...
py manage.py collectstatic --noinput

echo.
echo [3/6] Chạy migrations...
py manage.py migrate

echo.
echo [4/6] Tạo thư mục media...
if not exist "media\crawled_images" mkdir media\crawled_images

echo.
echo [5/6] Kiểm tra cấu hình...
py manage.py check --deploy

echo.
echo [6/6] Khởi động server...
echo ========================================
echo   Server đang khởi động...
echo   URL: http://localhost:8000
echo   URL mạng: http://0.0.0.0:8000
echo   Nhấn Ctrl+C để dừng server
echo ========================================
echo.
py manage.py runserver 0.0.0.0:8000

pause
