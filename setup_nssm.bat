@echo off
echo ========================================
echo   Setup NSSM cho Django Image Crawler
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

REM Đường dẫn NSSM hiện tại
set NSSM_SOURCE=D:\app\nssm\win64\nssm.exe
set NSSM_TARGET=C:\Windows\System32\nssm.exe

echo 🔍 Kiểm tra NSSM...
echo Nguồn: %NSSM_SOURCE%
echo Đích:  %NSSM_TARGET%
echo.

REM Kiểm tra file nguồn
if not exist "%NSSM_SOURCE%" (
    echo ❌ Không tìm thấy NSSM tại: %NSSM_SOURCE%
    echo.
    echo 💡 Hướng dẫn khắc phục:
    echo    1. Kiểm tra đường dẫn NSSM
    echo    2. Hoặc tải NSSM từ: https://nssm.cc/download
    echo    3. Giải nén vào thư mục D:\app\nssm\
    echo.
    pause
    exit /b 1
)

echo ✅ Tìm thấy NSSM tại: %NSSM_SOURCE%

REM Kiểm tra xem đã copy chưa
if exist "%NSSM_TARGET%" (
    echo ⚠️ NSSM đã tồn tại trong System32
    echo.
    echo 🔄 Bạn có muốn ghi đè không? (Y/N)
    set /p choice=Nhập lựa chọn: 
    if /i not "%choice%"=="Y" (
        echo ❌ Hủy bỏ copy NSSM
        goto :test_nssm
    )
)

echo.
echo 📋 Copy NSSM vào System32...
copy "%NSSM_SOURCE%" "%NSSM_TARGET%" >nul
if %errorlevel% equ 0 (
    echo ✅ Copy NSSM thành công!
) else (
    echo ❌ Lỗi khi copy NSSM!
    pause
    exit /b 1
)

:test_nssm
echo.
echo 🧪 Test NSSM...
nssm version
if %errorlevel% equ 0 (
    echo ✅ NSSM hoạt động bình thường!
) else (
    echo ❌ NSSM không hoạt động!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ Setup NSSM hoàn tất!
echo   
echo   📋 Bước tiếp theo:
echo   1. Chạy install_service.bat để cài service
echo   2. Hoặc sử dụng lệnh nssm trực tiếp
echo   
echo   💡 Lệnh NSSM cơ bản:
echo   - nssm install [servicename] [program]
echo   - nssm start [servicename]
echo   - nssm stop [servicename]
echo   - nssm remove [servicename]
echo ========================================
echo.
pause
