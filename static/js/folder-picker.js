/**
 * Folder Picker for Web Browser
 * Fallback solution cho việc chọn thư mục trong web browser
 */

class FolderPicker {
    constructor() {
        this.createFolderDialog();
    }

    createFolderDialog() {
        // Tạo modal dialog để nhập đường dẫn thư mục
        const modalHTML = `
            <div class="modal fade" id="folderPickerModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-folder-open"></i> Chọn thư mục lưu ảnh
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label class="form-label">Đường dẫn thư mục:</label>
                                <input type="text" class="form-control" id="folderPathInput" 
                                       placeholder="VD: C:/MyImages/ hoặc /home/user/Pictures/">
                                <div class="form-text">
                                    Nhập đường dẫn đầy đủ đến thư mục bạn muốn lưu ảnh
                                </div>
                            </div>
                            
                            <div class="alert alert-info">
                                <h6><i class="fas fa-lightbulb"></i> Gợi ý đường dẫn:</h6>
                                <ul class="mb-0">
                                    <li><strong>Windows:</strong> C:/Users/YourName/Pictures/CrawledImages/</li>
                                    <li><strong>Mac:</strong> /Users/YourName/Pictures/CrawledImages/</li>
                                    <li><strong>Linux:</strong> /home/YourName/Pictures/CrawledImages/</li>
                                </ul>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Hoặc chọn thư mục có sẵn:</label>
                                <div class="d-grid gap-2">
                                    <button class="btn btn-outline-primary" onclick="folderPicker.selectPredefinedFolder('downloads')">
                                        <i class="fas fa-download"></i> Thư mục Downloads
                                    </button>
                                    <button class="btn btn-outline-primary" onclick="folderPicker.selectPredefinedFolder('desktop')">
                                        <i class="fas fa-desktop"></i> Desktop
                                    </button>
                                    <button class="btn btn-outline-primary" onclick="folderPicker.selectPredefinedFolder('pictures')">
                                        <i class="fas fa-images"></i> Thư mục Pictures
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
                            <button type="button" class="btn btn-primary" onclick="folderPicker.confirmSelection()">
                                <i class="fas fa-check"></i> Chọn thư mục này
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Thêm modal vào body nếu chưa có
        if (!document.getElementById('folderPickerModal')) {
            document.body.insertAdjacentHTML('beforeend', modalHTML);
        }
    }

    showDialog() {
        const modal = new bootstrap.Modal(document.getElementById('folderPickerModal'));
        modal.show();
        
        // Focus vào input
        setTimeout(() => {
            document.getElementById('folderPathInput').focus();
        }, 500);
    }

    selectPredefinedFolder(type) {
        const input = document.getElementById('folderPathInput');
        let path = '';
        
        // Detect OS và tạo đường dẫn phù hợp
        const isWindows = navigator.platform.indexOf('Win') > -1;
        const isMac = navigator.platform.indexOf('Mac') > -1;
        
        if (isWindows) {
            const username = 'YourName'; // Placeholder
            switch(type) {
                case 'downloads':
                    path = `C:/Users/${username}/Downloads/CrawledImages/`;
                    break;
                case 'desktop':
                    path = `C:/Users/${username}/Desktop/CrawledImages/`;
                    break;
                case 'pictures':
                    path = `C:/Users/${username}/Pictures/CrawledImages/`;
                    break;
            }
        } else if (isMac) {
            const username = 'YourName'; // Placeholder
            switch(type) {
                case 'downloads':
                    path = `/Users/${username}/Downloads/CrawledImages/`;
                    break;
                case 'desktop':
                    path = `/Users/${username}/Desktop/CrawledImages/`;
                    break;
                case 'pictures':
                    path = `/Users/${username}/Pictures/CrawledImages/`;
                    break;
            }
        } else {
            // Linux
            const username = 'YourName'; // Placeholder
            switch(type) {
                case 'downloads':
                    path = `/home/${username}/Downloads/CrawledImages/`;
                    break;
                case 'desktop':
                    path = `/home/${username}/Desktop/CrawledImages/`;
                    break;
                case 'pictures':
                    path = `/home/${username}/Pictures/CrawledImages/`;
                    break;
            }
        }
        
        input.value = path;
        input.focus();
    }

    confirmSelection() {
        const path = document.getElementById('folderPathInput').value.trim();
        
        if (!path) {
            alert('Vui lòng nhập đường dẫn thư mục!');
            return;
        }
        
        // Validate đường dẫn cơ bản
        if (!this.isValidPath(path)) {
            alert('Đường dẫn không hợp lệ! Vui lòng kiểm tra lại.');
            return;
        }
        
        // Set giá trị vào input chính
        document.getElementById('id_custom_folder_path').value = path;
        
        // Đóng modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('folderPickerModal'));
        modal.hide();
        
        // Hiển thị thông báo
        this.showSuccessMessage(path);
    }

    isValidPath(path) {
        // Kiểm tra đường dẫn cơ bản
        const windowsPattern = /^[A-Za-z]:[\\\/].*$/;
        const unixPattern = /^\/.*$/;
        const relativePattern = /^\.\.?[\\\/].*$/;
        
        return windowsPattern.test(path) || unixPattern.test(path) || relativePattern.test(path);
    }

    showSuccessMessage(path) {
        // Tạo toast notification
        const toastHTML = `
            <div class="toast align-items-center text-white bg-success border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-check-circle"></i> Đã chọn thư mục: ${path}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        // Tạo container cho toast nếu chưa có
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Thêm toast
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        
        // Hiển thị toast
        const toastElement = toastContainer.lastElementChild;
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Xóa toast sau khi ẩn
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
}

// Khởi tạo folder picker
const folderPicker = new FolderPicker();
