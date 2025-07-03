# 🕷️ Django Image Crawler

A Django application for crawling and downloading images from any website with a user-friendly interface and real-time progress bar.

## ✨ Key Features

- 🔍 **Automatic image crawling** from any URL
- 📊 **Real-time progress bar** with detailed statistics
- 🎯 **Smart image filtering** by size and format
- 💾 **Automatic image download** to local machine
- 📱 **Responsive interface** with Bootstrap 5
- 📝 **Crawl history management** with admin panel
- 🚀 **High performance** with chunked download
- 🛡️ **Smart error handling** and retry mechanism

## 📋 System Requirements

- **Windows 10/11** (64-bit)
- **Python 3.8+** (recommended 3.11+)
- **RAM**: Minimum 2GB
- **Storage**: 500MB free space for application + image storage space

## 🚀 Quick Installation (For Beginners)

### Step 1: Install Python

1. **Download Python** from: https://python.org/downloads/
2. **Important**: ✅ Check "Add Python to PATH" during installation
3. **Verify installation**:
   ```bash
   py --version
   ```

### Step 2: Download project

```bash
# Clone repository (if you have Git)
git clone <repository-url>
cd D:\www\PycharmProjects\DjangoProject

# Or download ZIP and extract to D:\www\PycharmProjects\DjangoProject
```

### Step 3: Automatic installation

```bash
# Run setup file (Windows)
setup.bat
```

### Step 4: Run application

```bash
# Run development server
run_server.bat
```

**Access**: http://127.0.0.1:8000

## 🔧 Manual Installation (Detailed)

### 1. Environment setup

```bash
# Create virtual environment (recommended)
py -m venv venv
venv\Scripts\activate

# Install dependencies
py -m pip install -r requirements.txt
```

### 2. Database configuration

```bash
# Create migrations
py manage.py makemigrations

# Run migrations
py manage.py migrate

# Create superuser (optional)
py manage.py createsuperuser
```

### 3. Create media directory

```bash
mkdir media
mkdir media\crawled_images
```

### 4. Collect static files

```bash
py manage.py collectstatic --noinput
```

### 5. Run server

```bash
py manage.py runserver 0.0.0.0:8000
```

## 🏭 Production Deployment on Windows

### Option 1: Windows Service with NSSM

#### Step 1: Install NSSM
1. Download **NSSM** from: https://nssm.cc/download
2. Extract to directory (e.g., `D:\app\nssm\`)
3. **Option A**: Copy `nssm.exe` to `C:\Windows\System32\`
4. **Option B**: Run `setup_nssm.bat` for automatic copy
5. **Option C**: Update path in scripts (pre-configured for `D:\app\nssm\win64\`)

#### Step 2: Create Production Script

Create file `start_production.bat`:
```batch
@echo off
cd /d "C:\path\to\your\DjangoProject"
venv\Scripts\activate
set DJANGO_SETTINGS_MODULE=DjangoProject.settings_production
py manage.py migrate
py manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 --workers 4 DjangoProject.wsgi:application
```

#### Step 3: Install Service
```bash
# Method 1: Use automatic script (Recommended)
install_service.bat

# Method 2: Manual with Command Prompt as Administrator
nssm install DjangoImageCrawler "C:\path\to\your\DjangoProject\start_production.bat"
nssm set DjangoImageCrawler AppDirectory "C:\path\to\your\DjangoProject"
nssm set DjangoImageCrawler DisplayName "Django Image Crawler"
nssm set DjangoImageCrawler Description "Django Image Crawler Service"
nssm set DjangoImageCrawler Start SERVICE_AUTO_START
nssm start DjangoImageCrawler
```

**Note**: Scripts are pre-configured for NSSM at `D:\app\nssm\win64\nssm.exe`

### Option 2: IIS with FastCGI

#### Step 1: Install IIS
1. **Control Panel** → **Programs** → **Turn Windows features on/off**
2. Check: **Internet Information Services**
3. Check: **CGI** (under Application Development Features)

#### Step 2: Install wfastcgi
```bash
pip install wfastcgi
wfastcgi-enable
```

#### Step 3: Configure IIS
1. Open **IIS Manager**
2. **Add Website**:
   - **Site name**: Django Image Crawler
   - **Physical path**: `C:\path\to\your\DjangoProject`
   - **Port**: 80 or 8000

3. **Handler Mappings** → **Add Module Mapping**:
   - **Request path**: `*`
   - **Module**: FastCgiModule
   - **Executable**: `C:\path\to\python.exe|C:\path\to\wfastcgi.py`

### Option 3: Docker (Recommended)

#### Step 1: Install Docker Desktop
Download from: https://docker.com/products/docker-desktop

#### Step 2: Build and Run
```bash
# Build image
docker build -t django-image-crawler .

# Run container
docker run -d -p 8000:8000 --name image-crawler django-image-crawler

# Or use docker-compose
docker-compose up -d
```

## 🔧 Production Configuration

### Environment Variables
Create `.env` file:
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
# Install PostgreSQL
# Download from: https://postgresql.org/download/windows/

# Install psycopg2
pip install psycopg2-binary

# Update settings_production.py
```

### Reverse Proxy with Nginx
Create `nginx.conf` file:
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

## 📖 Usage Guide

### 1. Basic image crawling
1. Access: http://localhost:8000
2. Click **"Crawl Images"**
3. Enter website URL
4. Choose settings (quantity, size, format)
5. Click **"Start Crawling"**
6. Monitor real-time progress bar

### 2. View results
- **Image list**: `/images/`
- **Crawl history**: `/sessions/`
- **Image details**: Click on any image
- **Admin panel**: `/admin/` (requires superuser creation)

### 3. Progress Bar Demo
- Access: `/demo/progress/`
- Click **"Start Demo"** to view simulation

## 🛠️ Troubleshooting

### Common Issues

#### 1. Python not found
```bash
# Check Python
py --version
python --version

# If error, reinstall Python with "Add to PATH"
```

#### 2. Dependencies installation error
```bash
# Update pip
py -m pip install --upgrade pip

# Install packages individually
py -m pip install Django
py -m pip install requests beautifulsoup4 Pillow
```

#### 3. 403 Forbidden error when crawling
- Try with different URLs (e.g., unsplash.com, pixabay.com)
- Some websites block bots/crawlers
- Check error page details for solutions

#### 4. Database error
```bash
# Reset database
del db.sqlite3
py manage.py migrate
```

#### 5. Static files error
```bash
# Recollect static files
py manage.py collectstatic --clear --noinput
```

### Performance Tuning

#### 1. Increase crawling speed
- Reduce `timeout` in requests
- Increase number of `workers` in gunicorn
- Use SSD for media storage

#### 2. Memory optimization
- Limit `max_images` per crawl session
- Clean up old images periodically
- Use PostgreSQL database instead of SQLite

## 📁 Project Structure

```
DjangoProject/
├── DjangoProject/          # Main settings and configuration
│   ├── settings.py         # Development configuration
│   ├── settings_production.py  # Production configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI application
├── image_crawler/         # Main app
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── forms.py           # Form validation
│   ├── urls.py            # App URL routing
│   └── admin.py           # Admin interface
├── templates/             # HTML templates
│   └── image_crawler/     # App templates
├── media/                 # Crawled images
│   └── crawled_images/    # Image storage directory
├── staticfiles/           # Static files (CSS, JS)
├── requirements.txt       # Python dependencies
├── setup.bat             # Automatic installation script
├── run_server.bat        # Development server script
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose
└── README.md             # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Create Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Support

- **Issues**: Create issue on GitHub
- **Email**: your-email@example.com
- **Documentation**: Wiki on GitHub

## 🎯 Roadmap

- [ ] Video crawling support
- [ ] REST API for integration
- [ ] Scheduled crawling
- [ ] Cloud storage integration
- [ ] Machine learning image classification
- [ ] Mobile app

---

**Made with ❤️ using Django & Bootstrap**
