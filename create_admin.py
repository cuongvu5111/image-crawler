#!/usr/bin/env python
"""
Script để tạo tài khoản admin Django
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth.models import User

# Thông tin admin
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

# Xóa user cũ nếu có
if User.objects.filter(username=username).exists():
    User.objects.filter(username=username).delete()
    print(f"Đã xóa user cũ: {username}")

# Tạo superuser mới
user = User.objects.create_superuser(
    username=username,
    email=email,
    password=password
)

print("=" * 50)
print("✅ Tài khoản admin đã được tạo thành công!")
print("=" * 50)
print(f"🌐 URL Admin: http://127.0.0.1:8008/admin/")
print(f"👤 Username: {username}")
print(f"📧 Email: {email}")
print(f"🔑 Password: {password}")
print("=" * 50)
print("Bây giờ bạn có thể đăng nhập vào admin panel!")
