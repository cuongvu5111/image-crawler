# 🚀 Quick Start Guide

## Cài đặt nhanh (5 phút)

### 1. Cài đặt Python
- Tải từ: https://python.org/downloads/
- ✅ **Quan trọng**: Tick "Add Python to PATH"

### 2. Cài đặt project
```bash
# Clone hoặc tải ZIP project
cd DjangoProject

# Chạy setup tự động
setup.bat
```

### 3. Chạy ứng dụng
```bash
# Development mode
run_server.bat

# Truy cập: http://127.0.0.1:8000
```

## Production Setup (Windows Service)

### 1. Cài đặt NSSM
```bash
# Option A: Tự động (Khuyến nghị)
setup_nssm.bat

# Option B: Thủ công
# - Tải từ: https://nssm.cc/download
# - Giải nén vào D:\app\nssm\
# - Hoặc copy nssm.exe vào C:\Windows\System32\
```

### 2. Cài đặt service
```bash
# Chạy với quyền Administrator
install_service.bat
```

**Lưu ý**: Scripts đã cấu hình sẵn cho NSSM tại `D:\app\nssm\win64\nssm.exe`

### 3. Quản lý service
```bash
# Kiểm tra trạng thái
check_service.bat

# Gỡ bỏ service
uninstall_service.bat
```

## URLs quan trọng

- 🏠 **Trang chủ**: http://localhost:8000
- 🕷️ **Crawl ảnh**: http://localhost:8000/crawl/
- 📷 **Danh sách ảnh**: http://localhost:8000/images/
- 📊 **Lịch sử crawl**: http://localhost:8000/sessions/
- 🎮 **Demo progress**: http://localhost:8000/demo/progress/
- ⚙️ **Admin**: http://localhost:8000/admin/

## Troubleshooting

### Python không tìm thấy
```bash
# Kiểm tra
py --version

# Nếu lỗi, cài đặt lại Python với "Add to PATH"
```

### Service không khởi động
```bash
# Kiểm tra logs
check_service.bat

# Xem logs tại: logs/service_error.log
```

### Crawl bị lỗi 403
- Thử URL khác: unsplash.com, pixabay.com
- Một số trang web chặn crawler

## Files quan trọng

- `setup.bat` - Cài đặt tự động
- `run_server.bat` - Chạy development
- `start_production.bat` - Chạy production
- `install_service.bat` - Cài service
- `check_service.bat` - Kiểm tra service
- `README.md` - Hướng dẫn chi tiết
