# 🕷️ Django Image Crawler

Ứng dụng Django để crawl và tải ảnh từ bất kỳ trang web nào với giao diện thân thiện và progress bar realtime.

## ✨ Tính năng chính

- 🔍 **Crawl ảnh tự động** từ bất kỳ URL nào
- 📊 **Progress bar realtime** với thống kê chi tiết
- 🎯 **Lọc ảnh thông minh** theo kích thước, định dạng
- 💾 **Tải ảnh tự động** về máy local
- 📱 **Giao diện responsive** Bootstrap 5
- 📝 **Quản lý lịch sử** crawl với admin panel
- 🚀 **Performance cao** với chunked download
- 🛡️ **Xử lý lỗi thông minh** và retry mechanism

## 📋 Yêu cầu hệ thống

- **Windows 10/11** (64-bit)
- **Python 3.8+** (khuyến nghị 3.11+)
- **RAM**: Tối thiểu 2GB
- **Ổ cứng**: 500MB trống cho ứng dụng + không gian lưu ảnh

## 🚀 Cài đặt nhanh (Người mới)

### Bước 1: Cài đặt Python

1. **Tải Python** từ: https://python.org/downloads/
2. **Quan trọng**: ✅ Tick "Add Python to PATH" khi cài đặt
3. **Kiểm tra cài đặt**:
   ```bash
   py --version
   ```

### Bước 2: Tải project

```bash
# Clone repository (nếu có Git)
git clone <repository-url>
cd D:\www\PycharmProjects\DjangoProject

# Hoặc tải ZIP và giải nén vào D:\www\PycharmProjects\DjangoProject
```

### Bước 3: Cài đặt tự động

```bash
# Chạy file setup (Windows)
setup.bat
```

### Bước 4: Chạy ứng dụng

```bash
# Chạy server development
run_server.bat
```

**Truy cập**: http://127.0.0.1:8000

## 🔧 Cài đặt thủ công (Chi tiết)

### 1. Chuẩn bị môi trường

```bash
# Tạo virtual environment (khuyến nghị)
py -m venv venv
venv\Scripts\activate

# Cài đặt dependencies
py -m pip install -r requirements.txt
```

### 2. Cấu hình database

```bash
# Tạo migrations
py manage.py makemigrations

# Chạy migrations
py manage.py migrate

# Tạo superuser (tùy chọn)
py manage.py createsuperuser
```

### 3. Tạo thư mục media

```bash
mkdir media
mkdir media\crawled_images
```

### 4. Collect static files

```bash
py manage.py collectstatic --noinput
```

### 5. Chạy server

```bash
py manage.py runserver 0.0.0.0:8000
```

## 🏭 Production Deployment trên Windows

### Option 1: Windows Service với NSSM

#### Bước 1: Cài đặt NSSM
1. Tải **NSSM** từ: https://nssm.cc/download
2. Giải nén vào thư mục (VD: `D:\app\nssm\`)
3. **Option A**: Copy `nssm.exe` vào `C:\Windows\System32\`
4. **Option B**: Chạy `setup_nssm.bat` để tự động copy
5. **Option C**: Cập nhật đường dẫn trong scripts (đã cấu hình sẵn cho `D:\app\nssm\win64\`)

#### Bước 2: Tạo Production Script

Tạo file `start_production.bat`:
```batch
@echo off
cd /d "C:\path\to\your\DjangoProject"
venv\Scripts\activate
set DJANGO_SETTINGS_MODULE=DjangoProject.settings_production
py manage.py migrate
py manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 --workers 4 DjangoProject.wsgi:application
```

#### Bước 3: Cài đặt Service
```bash
# Cách 1: Sử dụng script tự động (Khuyến nghị)
install_service.bat

# Cách 2: Thủ công với Command Prompt as Administrator
nssm install DjangoImageCrawler "C:\path\to\your\DjangoProject\start_production.bat"
nssm set DjangoImageCrawler AppDirectory "C:\path\to\your\DjangoProject"
nssm set DjangoImageCrawler DisplayName "Django Image Crawler"
nssm set DjangoImageCrawler Description "Django Image Crawler Service"
nssm set DjangoImageCrawler Start SERVICE_AUTO_START
nssm start DjangoImageCrawler
```

**Lưu ý**: Scripts đã được cấu hình sẵn cho NSSM tại `D:\app\nssm\win64\nssm.exe`

### Option 2: IIS với FastCGI

#### Bước 1: Cài đặt IIS
1. **Control Panel** → **Programs** → **Turn Windows features on/off**
2. Tick: **Internet Information Services**
3. Tick: **CGI** (trong Application Development Features)

#### Bước 2: Cài đặt wfastcgi
```bash
pip install wfastcgi
wfastcgi-enable
```

#### Bước 3: Cấu hình IIS
1. Mở **IIS Manager**
2. **Add Website**:
   - **Site name**: Django Image Crawler
   - **Physical path**: `C:\path\to\your\DjangoProject`
   - **Port**: 80 hoặc 8000

3. **Handler Mappings** → **Add Module Mapping**:
   - **Request path**: `*`
   - **Module**: FastCgiModule
   - **Executable**: `C:\path\to\python.exe|C:\path\to\wfastcgi.py`

### Option 3: Docker (Khuyến nghị)

#### Bước 1: Cài đặt Docker Desktop
Tải từ: https://docker.com/products/docker-desktop

#### Bước 2: Build và Run
```bash
# Build image
docker build -t django-image-crawler .

# Run container
docker run -d -p 8000:8000 --name image-crawler django-image-crawler

# Hoặc dùng docker-compose
docker-compose up -d
```

## 🔧 Cấu hình Production

### Environment Variables
Tạo file `.env`:
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost
DB_NAME=image_crawler_prod
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### Database Production (PostgreSQL)
```bash
# Cài đặt PostgreSQL
# Download từ: https://postgresql.org/download/windows/

# Cài đặt psycopg2
pip install psycopg2-binary

# Cập nhật settings_production.py
```

### Reverse Proxy với Nginx
Tạo file `nginx.conf`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias C:/path/to/your/DjangoProject/staticfiles/;
    }

    location /media/ {
        alias C:/path/to/your/DjangoProject/media/;
    }
}
```

## 📖 Hướng dẫn sử dụng

### 1. Crawl ảnh cơ bản
1. Truy cập: http://localhost:8000
2. Click **"Crawl ảnh"**
3. Nhập URL trang web
4. Chọn cài đặt (số lượng, kích thước, định dạng)
5. Click **"Bắt đầu crawl"**
6. Theo dõi progress bar realtime

### 2. Xem kết quả
- **Danh sách ảnh**: `/images/`
- **Lịch sử crawl**: `/sessions/`
- **Chi tiết ảnh**: Click vào ảnh bất kỳ
- **Admin panel**: `/admin/` (cần tạo superuser)

### 3. Demo Progress Bar
- Truy cập: `/demo/progress/`
- Click **"Bắt đầu Demo"** để xem simulation

## 🛠️ Troubleshooting

### Lỗi thường gặp

#### 1. Python không được tìm thấy
```bash
# Kiểm tra Python
py --version
python --version

# Nếu lỗi, cài đặt lại Python với "Add to PATH"
```

#### 2. Lỗi cài đặt dependencies
```bash
# Cập nhật pip
py -m pip install --upgrade pip

# Cài đặt từng package
py -m pip install Django
py -m pip install requests beautifulsoup4 Pillow
```

#### 3. Lỗi 403 Forbidden khi crawl
- Thử với URL khác (VD: unsplash.com, pixabay.com)
- Một số trang web chặn bot/crawler
- Xem trang lỗi chi tiết để biết giải pháp

#### 4. Lỗi database
```bash
# Reset database
del db.sqlite3
py manage.py migrate
```

#### 5. Lỗi static files
```bash
# Collect lại static files
py manage.py collectstatic --clear --noinput
```

### Performance Tuning

#### 1. Tăng tốc độ crawl
- Giảm `timeout` trong requests
- Tăng số `workers` trong gunicorn
- Sử dụng SSD cho media storage

#### 2. Tối ưu memory
- Giới hạn `max_images` mỗi lần crawl
- Dọn dẹp ảnh cũ định kỳ
- Sử dụng database PostgreSQL thay vì SQLite

## 📁 Cấu trúc project

```
DjangoProject/
├── DjangoProject/          # Settings và cấu hình chính
│   ├── settings.py         # Cấu hình development
│   ├── settings_production.py  # Cấu hình production
│   ├── urls.py            # URL routing chính
│   └── wsgi.py            # WSGI application
├── image_crawler/         # App chính
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── forms.py           # Form validation
│   ├── urls.py            # URL routing app
│   └── admin.py           # Admin interface
├── templates/             # HTML templates
│   └── image_crawler/     # App templates
├── media/                 # Ảnh đã crawl
│   └── crawled_images/    # Thư mục lưu ảnh
├── staticfiles/           # Static files (CSS, JS)
├── requirements.txt       # Python dependencies
├── setup.bat             # Script cài đặt tự động
├── run_server.bat        # Script chạy development
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose
└── README.md             # File này
```

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Hỗ trợ

- **Issues**: Tạo issue trên GitHub
- **Email**: your-email@example.com
- **Documentation**: Wiki trên GitHub

## 🎯 Roadmap

- [ ] Hỗ trợ crawl video
- [ ] API REST cho integration
- [ ] Scheduled crawling
- [ ] Cloud storage integration
- [ ] Machine learning image classification
- [ ] Mobile app

---

**Made with ❤️ using Django & Bootstrap**
