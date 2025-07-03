from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re


class CrawlImageForm(forms.Form):
    """Form để nhập URL crawl ảnh"""
    
    url = forms.URLField(
        label="URL trang web",
        max_length=500,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com',
            'required': True
        }),
        help_text="Nhập URL của trang web bạn muốn crawl ảnh"
    )
    
    # Tùy chọn crawl
    max_images = forms.IntegerField(
        label="Số ảnh tối đa",
        min_value=1,
        max_value=100,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '100'
        }),
        help_text="Số lượng ảnh tối đa muốn tải (1-100)"
    )
    
    min_width = forms.IntegerField(
        label="Chiều rộng tối thiểu (px)",
        min_value=50,
        initial=200,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '50'
        }),
        help_text="Chỉ tải ảnh có chiều rộng >= giá trị này"
    )
    
    min_height = forms.IntegerField(
        label="Chiều cao tối thiểu (px)",
        min_value=50,
        initial=200,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '50'
        }),
        help_text="Chỉ tải ảnh có chiều cao >= giá trị này"
    )
    
    # Định dạng ảnh cho phép
    ALLOWED_FORMATS = [
        ('jpg', 'JPEG'),
        ('png', 'PNG'),
        ('gif', 'GIF'),
        ('webp', 'WebP'),
        ('bmp', 'BMP'),
    ]
    
    allowed_formats = forms.MultipleChoiceField(
        label="Định dạng ảnh cho phép",
        choices=ALLOWED_FORMATS,
        initial=['jpg', 'png'],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        help_text="Chọn các định dạng ảnh muốn tải"
    )
    
    # Tùy chọn lưu file
    download_images = forms.BooleanField(
        label="Tải ảnh về máy",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text="Có tải ảnh về thư mục local không"
    )

    def clean_url(self):
        """Validate URL"""
        url = self.cleaned_data.get('url')
        
        if not url:
            raise ValidationError("URL không được để trống")
        
        # Kiểm tra định dạng URL
        validator = URLValidator()
        try:
            validator(url)
        except ValidationError:
            raise ValidationError("URL không hợp lệ")
        
        # Kiểm tra protocol
        if not url.startswith(('http://', 'https://')):
            raise ValidationError("URL phải bắt đầu bằng http:// hoặc https://")
        
        return url

    def clean_allowed_formats(self):
        """Validate allowed formats"""
        formats = self.cleaned_data.get('allowed_formats')
        
        if not formats:
            raise ValidationError("Phải chọn ít nhất một định dạng ảnh")
        
        return formats

    def clean(self):
        """Validate toàn bộ form"""
        cleaned_data = super().clean()
        
        min_width = cleaned_data.get('min_width')
        min_height = cleaned_data.get('min_height')
        max_images = cleaned_data.get('max_images')
        
        # Kiểm tra kích thước hợp lý
        if min_width and min_width > 5000:
            raise ValidationError("Chiều rộng tối thiểu quá lớn (>5000px)")
        
        if min_height and min_height > 5000:
            raise ValidationError("Chiều cao tối thiểu quá lớn (>5000px)")
        
        # Kiểm tra số lượng ảnh
        if max_images and max_images > 100:
            raise ValidationError("Số ảnh tối đa không được vượt quá 100")
        
        return cleaned_data


class SearchImageForm(forms.Form):
    """Form tìm kiếm ảnh đã crawl"""
    
    search_query = forms.CharField(
        label="Tìm kiếm",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tìm theo tên ảnh hoặc URL...'
        })
    )
    
    status_filter = forms.ChoiceField(
        label="Trạng thái",
        choices=[('', 'Tất cả')] + [
            ('completed', 'Hoàn thành'),
            ('failed', 'Thất bại'),
            ('pending', 'Đang chờ'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    date_from = forms.DateField(
        label="Từ ngày",
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        label="Đến ngày",
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
