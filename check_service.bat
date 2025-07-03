@echo off
echo ========================================
echo   Kiểm tra Django Image Crawler Service
echo ========================================

echo.
echo 🔍 Kiểm tra trạng thái service...

REM Đường dẫn NSSM
set NSSM_PATH=D:\app\nssm\win64\nssm.exe

REM Kiểm tra NSSM
if not exist "%NSSM_PATH%" (
    echo ❌ NSSM không tìm thấy tại: %NSSM_PATH%
    echo 💡 Kiểm tra đường dẫn NSSM hoặc cài đặt NSSM
    echo.
    pause
    exit /b 1
)

"%NSSM_PATH%" version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ NSSM không thể chạy!
    echo.
    pause
    exit /b 1
)

REM Kiểm tra service
"%NSSM_PATH%" status DjangoImageCrawler >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Service DjangoImageCrawler không tồn tại
    echo 💡 Chạy install_service.bat để cài đặt service
    echo.
    pause
    exit /b 1
)

echo ✅ Service đã được cài đặt
echo.

echo 📊 Thông tin chi tiết service:
echo ----------------------------------------
echo Tên service: DjangoImageCrawler
echo Trạng thái:
"%NSSM_PATH%" status DjangoImageCrawler
echo.

echo 📁 Đường dẫn executable:
"%NSSM_PATH%" get DjangoImageCrawler Application
echo.

echo 📁 Thư mục làm việc:
"%NSSM_PATH%" get DjangoImageCrawler AppDirectory
echo.

echo 📝 Log files:
echo Stdout:
"%NSSM_PATH%" get DjangoImageCrawler AppStdout
echo Stderr:
"%NSSM_PATH%" get DjangoImageCrawler AppStderr
echo.

echo 🌐 Kiểm tra kết nối web...
echo Đang test kết nối đến http://localhost:8000...

REM Test kết nối bằng PowerShell
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 5 -UseBasicParsing; Write-Host '✅ Web server đang hoạt động - Status:' $response.StatusCode } catch { Write-Host '❌ Không thể kết nối đến web server' }"

echo.
echo 📋 Các lệnh quản lý service:
echo ----------------------------------------
echo 🚀 Khởi động:  "%NSSM_PATH%" start DjangoImageCrawler
echo 🛑 Dừng:       "%NSSM_PATH%" stop DjangoImageCrawler
echo 🔄 Restart:    "%NSSM_PATH%" restart DjangoImageCrawler
echo 📊 Trạng thái:  "%NSSM_PATH%" status DjangoImageCrawler
echo ⚙️ Cấu hình:   "%NSSM_PATH%" edit DjangoImageCrawler
echo ❌ Gỡ bỏ:      "%NSSM_PATH%" remove DjangoImageCrawler

echo.
echo 🔗 URLs hữu ích:
echo ----------------------------------------
echo 🏠 Trang chủ:        http://localhost:8000
echo 🕷️ Crawl ảnh:        http://localhost:8000/crawl/
echo 📷 Danh sách ảnh:    http://localhost:8000/images/
echo 📊 Lịch sử crawl:    http://localhost:8000/sessions/
echo ⚙️ Admin panel:      http://localhost:8000/admin/
echo 🎮 Demo progress:    http://localhost:8000/demo/progress/

echo.
echo 📝 Log files location:
set PROJECT_PATH=%~dp0
set PROJECT_PATH=%PROJECT_PATH:~0,-1%
echo 📁 %PROJECT_PATH%\logs\
if exist "%PROJECT_PATH%\logs\service_output.log" (
    echo ✅ Output log exists
) else (
    echo ⚠️ Output log not found
)
if exist "%PROJECT_PATH%\logs\service_error.log" (
    echo ✅ Error log exists  
) else (
    echo ⚠️ Error log not found
)

echo.
echo ========================================
pause
