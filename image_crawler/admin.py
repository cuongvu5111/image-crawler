from django.contrib import admin
from .models import CrawledImage, CrawlSession


@admin.register(CrawledImage)
class CrawledImageAdmin(admin.ModelAdmin):
    """Admin cho CrawledImage"""
    
    list_display = [
        'image_name', 'source_url', 'status', 'get_file_size_display', 
        'get_dimensions_display', 'crawled_at'
    ]
    
    list_filter = [
        'status', 'image_format', 'crawled_at'
    ]
    
    search_fields = [
        'image_name', 'source_url', 'image_url'
    ]
    
    readonly_fields = [
        'crawled_at', 'file_size', 'width', 'height', 'local_path'
    ]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('image_name', 'source_url', 'image_url', 'status')
        }),
        ('Thông tin file', {
            'fields': ('image_format', 'file_size', 'width', 'height', 'local_path')
        }),
        ('Thời gian & Lỗi', {
            'fields': ('crawled_at', 'error_message')
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_failed']
    
    def mark_as_completed(self, request, queryset):
        """Đánh dấu là hoàn thành"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'Đã cập nhật {updated} ảnh thành "Hoàn thành"')
    mark_as_completed.short_description = "Đánh dấu là hoàn thành"
    
    def mark_as_failed(self, request, queryset):
        """Đánh dấu là thất bại"""
        updated = queryset.update(status='failed')
        self.message_user(request, f'Đã cập nhật {updated} ảnh thành "Thất bại"')
    mark_as_failed.short_description = "Đánh dấu là thất bại"


@admin.register(CrawlSession)
class CrawlSessionAdmin(admin.ModelAdmin):
    """Admin cho CrawlSession"""
    
    list_display = [
        'target_url', 'status', 'total_images_found', 'images_downloaded', 
        'images_failed', 'get_success_rate', 'started_at'
    ]
    
    list_filter = [
        'status', 'started_at'
    ]
    
    search_fields = [
        'target_url', 'notes'
    ]
    
    readonly_fields = [
        'started_at', 'finished_at', 'get_duration', 'get_success_rate'
    ]
    
    fieldsets = (
        ('Thông tin crawl', {
            'fields': ('target_url', 'status', 'notes')
        }),
        ('Thống kê', {
            'fields': ('total_images_found', 'images_downloaded', 'images_failed', 'get_success_rate')
        }),
        ('Thời gian', {
            'fields': ('started_at', 'finished_at', 'get_duration')
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_failed']
    
    def mark_as_completed(self, request, queryset):
        """Đánh dấu là hoàn thành"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'Đã cập nhật {updated} phiên thành "Hoàn thành"')
    mark_as_completed.short_description = "Đánh dấu là hoàn thành"
    
    def mark_as_failed(self, request, queryset):
        """Đánh dấu là thất bại"""
        updated = queryset.update(status='failed')
        self.message_user(request, f'Đã cập nhật {updated} phiên thành "Thất bại"')
    mark_as_failed.short_description = "Đánh dấu là thất bại"
