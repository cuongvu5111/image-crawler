from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'image_crawler'

urlpatterns = [
    # Trang chủ
    path('', views.index, name='index'),
    
    # Crawl ảnh
    path('crawl/', views.crawl_images, name='crawl'),
    
    # Danh sách ảnh
    path('images/', views.image_list, name='image_list'),
    path('images/<int:image_id>/', views.image_detail, name='image_detail'),
    path('images/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    path('images/<int:image_id>/download/', views.download_image_file, name='download_image'),
    path('images/<int:image_id>/download-direct/', views.download_single_image_direct, name='download_image_direct'),
    
    # Phiên crawl
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:session_id>/', views.session_detail, name='session_detail'),
    path('sessions/<int:session_id>/download-zip/', views.download_images_zip, name='download_session_zip'),

    # Progress tracking
    path('progress/<int:session_id>/', views.crawl_progress_view, name='crawl_progress'),
    path('api/progress/<int:session_id>/', views.get_crawl_progress, name='crawl_progress_api'),

    # Demo
    path('demo/progress/', lambda request: render(request, 'image_crawler/progress_demo.html'), name='progress_demo'),
]
