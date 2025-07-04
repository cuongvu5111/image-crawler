﻿from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import pytz
import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import os
import urllib.parse
from urllib.parse import urljoin, urlparse
import mimetypes
import json
import zipfile
import tempfile
import threading
import time
from .models import CrawledImage, CrawlSession
from .forms import CrawlImageForm, SearchImageForm


def get_local_time_str(dt):
    """Convert UTC datetime to local timezone string"""
    if dt:
        # Convert to local timezone
        local_tz = pytz.timezone(settings.TIME_ZONE)
        local_dt = dt.astimezone(local_tz)
        return local_dt.strftime('%H:%M:%S')
    return ''


def index(request):
    """Trang chủ - hiển thị form crawl và danh sách ảnh gần đây"""
    form = CrawlImageForm()
    
    # Lấy 10 ảnh mới nhất
    recent_images = CrawledImage.objects.filter(status='completed')[:10]
    
    # Thống kê
    stats = {
        'total_images': CrawledImage.objects.count(),
        'completed_images': CrawledImage.objects.filter(status='completed').count(),
        'failed_images': CrawledImage.objects.filter(status='failed').count(),
        'total_sessions': CrawlSession.objects.count(),
    }
    
    context = {
        'form': form,
        'recent_images': recent_images,
        'stats': stats,
    }
    
    return render(request, 'image_crawler/index.html', context)


def crawl_images(request):
    """Xử lý crawl ảnh từ URL"""
    if request.method == 'POST':
        form = CrawlImageForm(request.POST)
        
        if form.is_valid():
            url = form.cleaned_data['url']
            max_images = form.cleaned_data['max_images']
            min_width = form.cleaned_data.get('min_width', 0)
            min_height = form.cleaned_data.get('min_height', 0)
            allowed_formats = form.cleaned_data['allowed_formats']
            download_option = form.cleaned_data.get('download_option', 'server')
            download_images = download_option in ['server', 'both']  # Tải về server nếu chọn server hoặc both
            save_folder = form.cleaned_data.get('save_folder', 'crawled_images')
            custom_folder_path = form.cleaned_data.get('custom_folder_path', '')
            
            # Tạo session crawl
            session = CrawlSession.objects.create(
                target_url=url,
                status='running'
            )
            
            try:
                # Kiểm tra nếu là AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    # Chạy crawl trong background thread
                    import threading

                    def background_crawl():
                        perform_image_crawl(
                            url, max_images, min_width, min_height,
                            allowed_formats, download_images, session,
                            save_folder, custom_folder_path
                        )

                    # Bắt đầu thread
                    thread = threading.Thread(target=background_crawl)
                    thread.daemon = True
                    thread.start()

                    # Trả về session_id để JavaScript có thể track progress
                    return JsonResponse({'session_id': session.id})

                # Crawl ảnh (cho non-AJAX request)
                result = perform_image_crawl(
                    url, max_images, min_width, min_height,
                    allowed_formats, download_images, session,
                    save_folder, custom_folder_path
                )

                # Redirect đến trang progress để theo dõi realtime
                return redirect('image_crawler:crawl_progress', session_id=session.id)

            except Exception as e:
                session.status = 'failed'
                session.finished_at = timezone.now()
                session.save()

                # Hiển thị trang lỗi chi tiết
                context = {
                    'error_message': f"Lỗi không mong muốn: {str(e)}",
                    'session': session,
                    'form': form
                }
                return render(request, 'image_crawler/crawl_error.html', context)
    
    else:
        # Pre-fill URL nếu có trong query parameter
        initial_data = {}
        if 'url' in request.GET:
            initial_data['url'] = request.GET['url']

        form = CrawlImageForm(initial=initial_data)

    return render(request, 'image_crawler/crawl.html', {'form': form})


def get_save_folder_path(save_folder, custom_path=None):
    """Lấy đường dẫn thư mục lưu ảnh"""
    if save_folder == 'crawled_images':
        # Thư mục mặc định
        folder_path = os.path.join(settings.MEDIA_ROOT, 'crawled_images')
    elif save_folder == 'downloads':
        # Thư mục Downloads
        folder_path = os.path.join(Path.home(), 'Downloads', 'CrawledImages')
    elif save_folder == 'desktop':
        # Desktop
        folder_path = os.path.join(Path.home(), 'Desktop', 'CrawledImages')
    elif save_folder == 'pictures':
        # Thư mục Pictures
        folder_path = os.path.join(Path.home(), 'Pictures', 'CrawledImages')
    elif save_folder == 'custom' and custom_path:
        # Thư mục tùy chọn
        folder_path = custom_path
    else:
        # Fallback về thư mục mặc định
        folder_path = os.path.join(settings.MEDIA_ROOT, 'crawled_images')

    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(folder_path, exist_ok=True)

    return folder_path


def perform_image_crawl(url, max_images, min_width, min_height, allowed_formats, download_images, session, save_folder='crawled_images', custom_path=None):
    """Thực hiện crawl ảnh từ URL"""
    try:
        # Lấy đường dẫn thư mục lưu ảnh
        save_folder_path = get_save_folder_path(save_folder, custom_path)

        # Cập nhật trạng thái bắt đầu
        session.notes = f'Đang kết nối đến trang web... (Lưu vào: {save_folder_path})'
        session.save()

        # Headers để giả lập browser thực
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        # Tạo session để duy trì cookies
        session_requests = requests.Session()
        session_requests.headers.update(headers)

        # Thêm delay để tránh bị chặn
        import time
        time.sleep(2)

        # Lấy nội dung trang với retry
        session.notes = 'Đang tải nội dung trang web...'
        session.save()

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = session_requests.get(url, timeout=30, allow_redirects=True)
                response.raise_for_status()
                break
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    if attempt < max_retries - 1:
                        # Thử với headers khác
                        session_requests.headers.update({
                            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{120 + attempt}.0.0.0 Safari/537.36',
                            'Referer': 'https://www.google.com/'
                        })
                        time.sleep(5)  # Đợi lâu hơn
                        continue
                    else:
                        raise Exception(f"Trang web từ chối truy cập (403 Forbidden). Có thể trang web này chặn bot/crawler. Hãy thử với URL khác.")
                else:
                    raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                else:
                    raise e
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tìm tất cả thẻ img
        img_tags = soup.find_all('img')
        
        found_count = 0
        downloaded_count = 0
        failed_count = 0

        # Cập nhật session với tổng số ảnh tìm thấy
        total_images = len(img_tags[:max_images])
        session.total_images_found = total_images
        session.save()

        for index, img_tag in enumerate(img_tags[:max_images], 1):
            if found_count >= max_images:
                break

            # Cập nhật progress trong session notes
            progress_percent = int((index / total_images) * 100)
            session.notes = f"Đang phân tích ảnh {index}/{total_images} ({progress_percent}%)"
            session.save()

            # Lấy URL ảnh
            img_url = img_tag.get('src') or img_tag.get('data-src')
            if not img_url:
                continue

            # Chuyển đổi relative URL thành absolute URL
            img_url = urljoin(url, img_url)

            # Kiểm tra định dạng ảnh
            parsed_url = urlparse(img_url)
            file_extension = os.path.splitext(parsed_url.path)[1].lower().lstrip('.')

            if file_extension not in allowed_formats:
                continue

            found_count += 1

            # Tạo record trong database
            img_name = os.path.basename(parsed_url.path) or f"image_{found_count}.{file_extension}"

            crawled_image = CrawledImage.objects.create(
                source_url=url,
                image_url=img_url,
                image_name=img_name,
                image_format=file_extension,
                status='pending'
            )

            # Download ảnh nếu được yêu cầu
            if download_images:
                try:
                    # Cập nhật trạng thái downloading
                    crawled_image.status = 'downloading'
                    crawled_image.save()

                    session.notes = f"Đang tải ảnh {downloaded_count + 1}/{found_count}: {img_name}"
                    session.save()

                    download_result = download_image(crawled_image, headers, session, downloaded_count + 1, found_count, save_folder_path)
                    if download_result:
                        downloaded_count += 1
                        session.images_downloaded = downloaded_count
                    else:
                        failed_count += 1
                        session.images_failed = failed_count
                    session.save()
                except Exception as e:
                    crawled_image.status = 'failed'
                    crawled_image.error_message = str(e)
                    crawled_image.save()
                    failed_count += 1
                    session.images_failed = failed_count
                    session.save()
            else:
                crawled_image.status = 'completed'
                crawled_image.save()
                downloaded_count += 1
                session.images_downloaded = downloaded_count
                session.save()
        
        # Cập nhật session
        session.total_images_found = found_count
        session.images_downloaded = downloaded_count
        session.images_failed = failed_count
        session.status = 'completed'
        session.finished_at = timezone.now()
        session.save()
        
        return {
            'success': True,
            'found': found_count,
            'downloaded': downloaded_count,
            'failed': failed_count
        }
        
    except Exception as e:
        session.status = 'failed'
        session.finished_at = timezone.now()
        session.notes = str(e)
        session.save()
        
        return {
            'success': False,
            'error': str(e)
        }


def download_image(crawled_image, headers, session=None, current_index=1, total_count=1, save_folder_path=None):
    """Download ảnh và lưu vào local với progress tracking"""
    try:
        crawled_image.status = 'downloading'
        crawled_image.save()

        # Cập nhật progress trong session
        if session:
            progress_percent = int((current_index / total_count) * 100)
            session.notes = f"📥 Đang tải ảnh {current_index}/{total_count} ({progress_percent}%): {crawled_image.image_name}"
            session.save()

        # Tạo thư mục lưu ảnh
        if save_folder_path:
            media_dir = save_folder_path
        else:
            media_dir = os.path.join(settings.BASE_DIR, 'media', 'crawled_images')
        os.makedirs(media_dir, exist_ok=True)

        # Download ảnh với progress tracking
        response = requests.get(crawled_image.image_url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()

        # Lấy tổng kích thước file
        total_size = int(response.headers.get('content-length', 0))

        # Lưu file với progress tracking
        file_path = os.path.join(media_dir, crawled_image.image_name)
        downloaded_size = 0

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    # Cập nhật progress download
                    if session and total_size > 0:
                        file_progress = int((downloaded_size / total_size) * 100)
                        session.notes = f"📥 Đang tải {crawled_image.image_name} ({file_progress}%) - Ảnh {current_index}/{total_count}"
                        session.save()

        # Lấy thông tin ảnh
        try:
            with Image.open(file_path) as img:
                crawled_image.width = img.width
                crawled_image.height = img.height
        except:
            pass

        crawled_image.local_path = file_path
        crawled_image.file_size = downloaded_size
        crawled_image.status = 'completed'
        crawled_image.save()

        # Cập nhật hoàn thành
        if session:
            session.notes = f"✅ Đã tải xong: {crawled_image.image_name} ({current_index}/{total_count})"
            session.save()

        return True

    except Exception as e:
        crawled_image.status = 'failed'
        crawled_image.error_message = str(e)
        crawled_image.save()

        # Cập nhật lỗi
        if session:
            session.notes = f"❌ Lỗi tải ảnh: {crawled_image.image_name} - {str(e)}"
            session.save()

        return False


def get_crawl_progress(request, session_id):
    """API để lấy tiến trình crawl realtime"""
    try:
        session = get_object_or_404(CrawlSession, id=session_id)
        # Refresh dữ liệu từ database để đảm bảo có dữ liệu mới nhất
        session.refresh_from_db()

        # Tính toán progress
        total_progress = 0
        if session.total_images_found > 0:
            total_progress = int(((session.images_downloaded + session.images_failed) / session.total_images_found) * 100)

        # Lấy log từ các ảnh đã crawl gần đây (theo URL)
        recent_images = CrawledImage.objects.filter(source_url=session.target_url).order_by('-crawled_at')[:5]
        log_entries = []

        for img in recent_images:
            if img.status == 'completed':
                log_entries.append({
                    'time': get_local_time_str(img.crawled_at),
                    'message': f'✅ Đã tải: {img.image_name}',
                    'type': 'success'
                })
            elif img.status == 'failed':
                log_entries.append({
                    'time': get_local_time_str(img.crawled_at),
                    'message': f'❌ Lỗi: {img.image_name} - {img.error_message or "Không xác định"}',
                    'type': 'danger'
                })
            elif img.status == 'downloading':
                log_entries.append({
                    'time': get_local_time_str(img.crawled_at),
                    'message': f'⬇️ Đang tải: {img.image_name}',
                    'type': 'info'
                })

        data = {
            'status': session.status,
            'total_found': session.total_images_found,
            'downloaded': session.images_downloaded,
            'failed': session.images_failed,
            'progress': total_progress,
            'current_task': session.notes or 'Đang khởi tạo...',
            'is_completed': session.status in ['completed', 'failed', 'cancelled'],
            'log_entries': log_entries,
            'current_image': recent_images.first().image_name if recent_images.exists() else None
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def crawl_progress_view(request, session_id):
    """Hiển thị trang theo dõi tiến trình crawl"""
    session = get_object_or_404(CrawlSession, id=session_id)

    # Nếu session chưa hoàn thành, bắt đầu crawl trong background
    if session.status == 'running':
        # Import threading để chạy crawl trong background
        import threading

        # Lấy thông tin từ session để crawl
        # (Cần lưu thông tin crawl vào session hoặc database)

        def background_crawl():
            try:
                # Thực hiện crawl (cần truyền đúng parameters)
                # Tạm thời để trống, sẽ implement sau
                pass
            except Exception as e:
                session.status = 'failed'
                session.notes = f"Lỗi: {str(e)}"
                session.finished_at = timezone.now()
                session.save()

        # Chạy crawl trong background thread
        thread = threading.Thread(target=background_crawl)
        thread.daemon = True
        thread.start()

    return render(request, 'image_crawler/crawl_progress.html', {'session': session})


def image_list(request):
    """Danh sách ảnh đã crawl với tìm kiếm và phân trang"""
    form = SearchImageForm(request.GET)
    images = CrawledImage.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        status_filter = form.cleaned_data.get('status_filter')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if search_query:
            images = images.filter(
                Q(image_name__icontains=search_query) |
                Q(source_url__icontains=search_query) |
                Q(image_url__icontains=search_query)
            )

        if status_filter:
            images = images.filter(status=status_filter)

        if date_from:
            images = images.filter(crawled_at__date__gte=date_from)

        if date_to:
            images = images.filter(crawled_at__date__lte=date_to)

    # Phân trang
    paginator = Paginator(images, 20)  # 20 ảnh mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'images': page_obj,
    }

    return render(request, 'image_crawler/image_list.html', context)


def image_detail(request, image_id):
    """Chi tiết ảnh"""
    image = get_object_or_404(CrawledImage, id=image_id)

    context = {
        'image': image,
    }

    return render(request, 'image_crawler/image_detail.html', context)


def session_list(request):
    """Danh sách phiên crawl"""
    sessions = CrawlSession.objects.all()

    # Phân trang
    paginator = Paginator(sessions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sessions': page_obj,
    }

    return render(request, 'image_crawler/session_list.html', context)


def session_detail(request, session_id):
    """Chi tiết phiên crawl"""
    session = get_object_or_404(CrawlSession, id=session_id)

    # Lấy ảnh của phiên này
    images = CrawledImage.objects.filter(
        source_url=session.target_url,
        crawled_at__gte=session.started_at
    )

    if session.finished_at:
        images = images.filter(crawled_at__lte=session.finished_at)

    # Phân trang
    paginator = Paginator(images, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'session': session,
        'page_obj': page_obj,
        'images': page_obj,
    }

    return render(request, 'image_crawler/session_detail.html', context)


@csrf_exempt
def delete_image(request, image_id):
    """Xóa ảnh"""
    if request.method == 'POST':
        image = get_object_or_404(CrawledImage, id=image_id)

        # Xóa file local nếu có
        if image.local_path and os.path.exists(image.local_path):
            try:
                os.remove(image.local_path)
            except:
                pass

        image.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        else:
            messages.success(request, 'Đã xóa ảnh thành công!')
            return redirect('image_crawler:image_list')

    return JsonResponse({'success': False, 'error': 'Method not allowed'})


def download_image_file(request, image_id):
    """Download file ảnh"""
    image = get_object_or_404(CrawledImage, id=image_id)

    if not image.local_path or not os.path.exists(image.local_path):
        messages.error(request, 'File ảnh không tồn tại!')
        return redirect('image_crawler:image_detail', image_id=image_id)

    try:
        with open(image.local_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{image.image_name}"'
            return response
    except Exception as e:
        messages.error(request, f'Lỗi khi tải file: {str(e)}')
        return redirect('image_crawler:image_detail', image_id=image_id)


def download_images_zip(request, session_id):
    """Tạo và download file ZIP chứa tất cả ảnh từ một session crawl"""
    session = get_object_or_404(CrawlSession, id=session_id)

    # Lấy tất cả ảnh đã download thành công từ session này
    images = CrawledImage.objects.filter(
        source_url=session.target_url,
        status='completed',
        local_path__isnull=False
    ).exclude(local_path='')

    if not images.exists():
        messages.error(request, 'Không có ảnh nào để tải về!')
        return redirect('image_crawler:session_detail', session_id=session_id)

    # Tạo file ZIP tạm thời
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')

    try:
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for image in images:
                if os.path.exists(image.local_path):
                    # Thêm file vào ZIP với tên gốc
                    zip_file.write(image.local_path, image.image_name)

        # Đọc file ZIP và trả về response
        with open(temp_zip.name, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')

            # Tạo tên file ZIP
            domain = urlparse(session.target_url).netloc or 'images'
            timestamp = session.started_at.strftime('%Y%m%d_%H%M%S')
            filename = f"{domain}_{timestamp}_images.zip"

            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

    except Exception as e:
        messages.error(request, f'Lỗi khi tạo file ZIP: {str(e)}')
        return redirect('image_crawler:session_detail', session_id=session_id)

    finally:
        # Xóa file tạm
        try:
            os.unlink(temp_zip.name)
        except:
            pass


def download_single_image_direct(request, image_id):
    """Download trực tiếp một ảnh từ URL gốc về máy người dùng"""
    image = get_object_or_404(CrawledImage, id=image_id)

    try:
        # Headers để giả lập browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Download ảnh từ URL gốc
        response = requests.get(image.image_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Tạo HTTP response để download
        http_response = HttpResponse(response.content, content_type=response.headers.get('content-type', 'application/octet-stream'))
        http_response['Content-Disposition'] = f'attachment; filename="{image.image_name}"'

        return http_response

    except Exception as e:
        messages.error(request, f'Lỗi khi tải ảnh: {str(e)}')
        return redirect('image_crawler:image_detail', image_id=image_id)
