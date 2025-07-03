from django.db import models
from django.utils import timezone
import os


class CrawledImage(models.Model):
    """Model để lưu thông tin ảnh đã crawl"""

    # URL gốc của trang web
    source_url = models.URLField(verbose_name="URL nguồn", max_length=500)
    
    # URL trực tiếp của ảnh
    image_url = models.URLField(verbose_name="URL ảnh", max_length=500)
    
    # Tên file ảnh
    image_name = models.CharField(verbose_name="Tên ảnh", max_length=255)
    
    # Đường dẫn lưu file local
    local_path = models.CharField(verbose_name="Đường dẫn local", max_length=500, blank=True)
    
    # Kích thước file (bytes)
    file_size = models.PositiveIntegerField(verbose_name="Kích thước file", null=True, blank=True)
    
    # Kích thước ảnh (width x height)
    width = models.PositiveIntegerField(verbose_name="Chiều rộng", null=True, blank=True)
    height = models.PositiveIntegerField(verbose_name="Chiều cao", null=True, blank=True)
    
    # Định dạng ảnh (jpg, png, gif, etc.)
    image_format = models.CharField(verbose_name="Định dạng", max_length=10, blank=True)
    
    # Thời gian crawl
    crawled_at = models.DateTimeField(verbose_name="Thời gian crawl", default=timezone.now)
    
    # Trạng thái download
    STATUS_CHOICES = [
        ('pending', 'Đang chờ'),
        ('downloading', 'Đang tải'),
        ('completed', 'Hoàn thành'),
        ('failed', 'Thất bại'),
    ]
    status = models.CharField(
        verbose_name="Trạng thái",
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Thông báo lỗi (nếu có)
    error_message = models.TextField(verbose_name="Thông báo lỗi", blank=True)

    class Meta:
        verbose_name = "Ảnh đã crawl"
        verbose_name_plural = "Ảnh đã crawl"
        ordering = ['-crawled_at']

    def __str__(self):
        return f"{self.image_name} - {self.source_url}"

    def get_file_size_display(self):
        """Hiển thị kích thước file dễ đọc"""
        if not self.file_size:
            return "Không xác định"
        
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"

    def get_dimensions_display(self):
        """Hiển thị kích thước ảnh"""
        if self.width and self.height:
            return f"{self.width} x {self.height}"
        return "Không xác định"


class CrawlSession(models.Model):
    """Model để lưu thông tin phiên crawl"""
    
    # URL được crawl
    target_url = models.URLField(verbose_name="URL mục tiêu", max_length=500)
    
    # Thời gian bắt đầu
    started_at = models.DateTimeField(verbose_name="Bắt đầu", default=timezone.now)
    
    # Thời gian kết thúc
    finished_at = models.DateTimeField(verbose_name="Kết thúc", null=True, blank=True)
    
    # Tổng số ảnh tìm thấy
    total_images_found = models.PositiveIntegerField(verbose_name="Tổng ảnh tìm thấy", default=0)
    
    # Số ảnh download thành công
    images_downloaded = models.PositiveIntegerField(verbose_name="Ảnh đã tải", default=0)
    
    # Số ảnh thất bại
    images_failed = models.PositiveIntegerField(verbose_name="Ảnh thất bại", default=0)
    
    # Trạng thái phiên crawl
    STATUS_CHOICES = [
        ('running', 'Đang chạy'),
        ('completed', 'Hoàn thành'),
        ('failed', 'Thất bại'),
        ('cancelled', 'Đã hủy'),
    ]
    status = models.CharField(
        verbose_name="Trạng thái",
        max_length=20,
        choices=STATUS_CHOICES,
        default='running'
    )
    
    # Ghi chú
    notes = models.TextField(verbose_name="Ghi chú", blank=True)

    class Meta:
        verbose_name = "Phiên crawl"
        verbose_name_plural = "Phiên crawl"
        ordering = ['-started_at']

    def __str__(self):
        return f"Crawl {self.target_url} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"

    def get_duration(self):
        """Tính thời gian crawl"""
        if self.finished_at:
            duration = self.finished_at - self.started_at
            return str(duration).split('.')[0]  # Bỏ microseconds
        return "Đang chạy"

    def get_success_rate(self):
        """Tính tỷ lệ thành công"""
        if self.total_images_found > 0:
            return f"{(self.images_downloaded / self.total_images_found * 100):.1f}%"
        return "0%"
