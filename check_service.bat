@echo off
echo ========================================
echo   Kiem tra Django Image Crawler Service
echo ========================================

echo.
echo Kiem tra trang thai service...

REM Đường dẫn NSSM
set NSSM_PATH=D:\app\nssm\win64\nssm.exe

REM Kiểm tra NSSM
if not exist "%NSSM_PATH%" (
    echo NSSM khong tim thay tai: %NSSM_PATH%
    echo Kiem tra duong dan NSSM hoac cai dat NSSM
    echo.
    pause
    exit /b 1
)

"%NSSM_PATH%" version >nul 2>&1
if %errorlevel% neq 0 (
    echo NSSM khong the chay!
    echo.
    pause
    exit /b 1
)

REM Kiểm tra service
"%NSSM_PATH%" status DjangoImageCrawler >nul 2>&1
if %errorlevel% neq 0 (
    echo Service DjangoImageCrawler khong ton tai
    echo Chay install_service.bat de cai dat service
    echo.
    pause
    exit /b 1
)

echo Service da duoc cai dat
echo.

echo Thong tin chi tiet service:
echo ----------------------------------------
echo Ten service: DjangoImageCrawler
echo Trang thai:
"%NSSM_PATH%" status DjangoImageCrawler
echo.

echo Duong dan executable:
"%NSSM_PATH%" get DjangoImageCrawler Application
echo.

echo Thu muc lam viec:
"%NSSM_PATH%" get DjangoImageCrawler AppDirectory
echo.

echo Log files:
echo Stdout:
"%NSSM_PATH%" get DjangoImageCrawler AppStdout
echo Stderr:
"%NSSM_PATH%" get DjangoImageCrawler AppStderr
echo.

echo Kiem tra ket noi web...
echo Dang test ket noi den http://localhost:8000...

REM Test kết nối bằng PowerShell
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 5 -UseBasicParsing; Write-Host 'Web server dang hoat dong - Status:' $response.StatusCode } catch { Write-Host 'Khong the ket noi den web server' }"

echo.
echo Cac lenh quan ly service:
echo ----------------------------------------
echo Khoi dong:  "%NSSM_PATH%" start DjangoImageCrawler
echo Dung:       "%NSSM_PATH%" stop DjangoImageCrawler
echo Restart:    "%NSSM_PATH%" restart DjangoImageCrawler
echo Trang thai: "%NSSM_PATH%" status DjangoImageCrawler
echo Cau hinh:   "%NSSM_PATH%" edit DjangoImageCrawler
echo Go bo:      "%NSSM_PATH%" remove DjangoImageCrawler

echo.
echo URLs huu ich:
echo ----------------------------------------
echo Trang chu:        http://localhost:8000
echo Crawl anh:        http://localhost:8000/crawl/
echo Danh sach anh:    http://localhost:8000/images/
echo Lich su crawl:    http://localhost:8000/sessions/
echo Admin panel:      http://localhost:8000/admin/
echo Demo progress:    http://localhost:8000/demo/progress/

echo.
echo Log files location:
set PROJECT_PATH=%~dp0
set PROJECT_PATH=%PROJECT_PATH:~0,-1%
echo %PROJECT_PATH%\logs\
if exist "%PROJECT_PATH%\logs\service_output.log" (
    echo Output log exists
) else (
    echo Output log not found
)
if exist "%PROJECT_PATH%\logs\service_error.log" (
    echo Error log exists
) else (
    echo Error log not found
)

echo.
echo ========================================
pause
