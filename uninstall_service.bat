@echo off
echo ========================================
echo   Gỡ bỏ Django Image Crawler Service
echo ========================================

REM Kiểm tra quyền Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Lỗi: Cần chạy với quyền Administrator!
    echo 💡 Cách khắc phục:
    echo    1. Click phải vào file này
    echo    2. Chọn "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Đang chạy với quyền Administrator
echo.

REM Đường dẫn NSSM
set NSSM_PATH=D:\app\nssm\win64\nssm.exe

REM Kiểm tra NSSM
if not exist "%NSSM_PATH%" (
    echo ❌ NSSM không tìm thấy tại: %NSSM_PATH%
    echo 💡 Kiểm tra đường dẫn NSSM
    echo.
    pause
    exit /b 1
)

REM Kiểm tra service có tồn tại không
"%NSSM_PATH%" status DjangoImageCrawler >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Service DjangoImageCrawler không tồn tại hoặc chưa được cài đặt
    echo.
    pause
    exit /b 0
)

echo 📊 Trạng thái service hiện tại:
"%NSSM_PATH%" status DjangoImageCrawler
echo.

echo 🛑 Dừng service...
"%NSSM_PATH%" stop DjangoImageCrawler
if %errorlevel% equ 0 (
    echo ✅ Service đã được dừng
) else (
    echo ⚠️ Service có thể đã dừng từ trước
)

echo.
echo 🗑️ Gỡ bỏ service...
"%NSSM_PATH%" remove DjangoImageCrawler confirm
if %errorlevel% equ 0 (
    echo ✅ Service đã được gỡ bỏ thành công!
) else (
    echo ❌ Lỗi khi gỡ bỏ service
)

echo.
echo ========================================
echo   ✅ Hoàn tất gỡ bỏ service
echo   
echo   💡 Lưu ý:
echo   - Project files vẫn còn nguyên
echo   - Logs vẫn được giữ lại
echo   - Có thể cài đặt lại bằng install_service.bat
echo ========================================
echo.
pause
