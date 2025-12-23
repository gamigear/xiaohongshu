// XHS Queue Manager Web App
const API_BASE = '/api';

// Global state
let currentData = {
    queue: [],
    stats: { pending: 0, done: 0, error: 0 },
    categories: [],
    config: {}
};

// Utility functions
function showAlert(containerId, message, type = 'info') {
    const container = document.getElementById(containerId);
    const alertClass = `alert-${type}`;
    container.innerHTML = `<div class="alert ${alertClass}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 5000);
}

function formatDate(dateString) {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleString('vi-VN');
}

function formatUrl(url, maxLength = 50) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// Tab management
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        
        // Update tab buttons
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName + 'Tab').classList.add('active');
        
        // Load data for specific tabs
        if (tabName === 'queue') {
            loadQueue();
        } else if (tabName === 'add') {
            loadCategories();
        } else if (tabName === 'config') {
            loadConfig();
        } else if (tabName === 'categories') {
            loadCategories();
        }
    });
});

// API functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(API_BASE + endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Load queue data
async function loadQueue() {
    try {
        const data = await apiCall('/queue');
        currentData.queue = data.items;
        currentData.stats = data.stats;
        
        updateStats();
        renderQueue();
    } catch (error) {
        document.getElementById('queueContent').innerHTML = 
            `<div class="alert alert-error">❌ Lỗi tải dữ liệu: ${error.message}</div>`;
    }
}

// Load categories
async function loadCategories() {
    try {
        const categories = await apiCall('/categories');
        currentData.categories = categories;
        
        updateCategorySelect();
        renderCategories();
        updateStats();
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load config
async function loadConfig() {
    try {
        const config = await apiCall('/config');
        currentData.config = config;
        
        document.getElementById('downloadPath').value = config.download_path || '/app/Volume/Download';
        document.getElementById('delaySeconds').value = config.delay_seconds || 120;
    } catch (error) {
        showAlert('configAlert', `❌ Lỗi tải config: ${error.message}`, 'error');
    }
}

// Update stats display
function updateStats() {
    document.getElementById('statPending').textContent = currentData.stats.pending;
    document.getElementById('statDone').textContent = currentData.stats.done;
    document.getElementById('statError').textContent = currentData.stats.error;
    document.getElementById('statCategories').textContent = currentData.categories.length;
}

// Render queue table
function renderQueue() {
    const container = document.getElementById('queueContent');
    
    if (currentData.queue.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p>Không có item nào trong hàng đợi</p>
            </div>
        `;
        return;
    }
    
    const tableHTML = `
        <table class="queue-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>URL</th>
                    <th>Category</th>
                    <th>Trạng thái</th>
                    <th>Tiêu đề</th>
                    <th>Tác giả</th>
                    <th>Thời gian</th>
                    <th>Thao tác</th>
                </tr>
            </thead>
            <tbody>
                ${currentData.queue.map(item => `
                    <tr>
                        <td>${item.id}</td>
                        <td class="url-cell" title="${item.url}">${formatUrl(item.url)}</td>
                        <td><span class="category-badge">${item.category || 'default'}</span></td>
                        <td><span class="status-badge status-${item.status}">${getStatusText(item.status)}</span></td>
                        <td>${item.title || '-'}</td>
                        <td>${item.author || '-'}</td>
                        <td>${formatDate(item.created_at)}</td>
                        <td>
                            ${item.status === 'pending' ? 
                                `<button class="btn btn-danger" onclick="deleteItem(${item.id})" style="padding: 4px 8px; font-size: 12px;">✕</button>` : 
                                '-'
                            }
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = tableHTML;
}

// Render categories
function renderCategories() {
    const container = document.getElementById('categoriesContent');
    
    if (currentData.categories.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3 7v10a2 2 0 002 2h10a2 2 0 002-2V9a2 2 0 00-2-2h-1V5a3 3 0 00-3-3H9a3 3 0 00-3 3v2H5a2 2 0 00-2 2z"></path>
                </svg>
                <p>Chưa có category nào</p>
            </div>
        `;
        return;
    }
    
    const cardsHTML = currentData.categories.map(cat => `
        <div class="stat-card" style="margin-bottom: 15px;">
            <div class="stat-number" style="color: #74b9ff;">${cat.count}</div>
            <div class="stat-label">📁 ${cat.name}</div>
        </div>
    `).join('');
    
    container.innerHTML = `<div class="stats-grid">${cardsHTML}</div>`;
}

// Update category select
function updateCategorySelect() {
    const select = document.getElementById('categorySelect');
    const currentValue = select.value;
    
    select.innerHTML = '<option value="default">default</option>';
    
    currentData.categories.forEach(cat => {
        if (cat.name !== 'default') {
            const option = document.createElement('option');
            option.value = cat.name;
            option.textContent = `${cat.name} (${cat.count})`;
            select.appendChild(option);
        }
    });
    
    // Restore selection
    if (currentValue) {
        select.value = currentValue;
    }
}

// Helper functions
function getStatusText(status) {
    const statusMap = {
        'pending': 'Đang chờ',
        'done': 'Hoàn thành',
        'error': 'Lỗi'
    };
    return statusMap[status] || status;
}

// Event handlers
async function refreshQueue() {
    await loadQueue();
    showAlert('queueContent', '🔄 Đã refresh dữ liệu', 'success');
}

async function clearPending() {
    if (!confirm('Bạn có chắc muốn xóa tất cả item pending?')) return;
    
    try {
        await apiCall('/queue', { method: 'DELETE' });
        await loadQueue();
        showAlert('queueContent', '🗑️ Đã xóa tất cả pending', 'success');
    } catch (error) {
        showAlert('queueContent', `❌ Lỗi: ${error.message}`, 'error');
    }
}

async function deleteItem(id) {
    if (!confirm('Bạn có chắc muốn xóa item này?')) return;
    
    try {
        await apiCall(`/queue/${id}`, { method: 'DELETE' });
        await loadQueue();
        showAlert('queueContent', '✅ Đã xóa item', 'success');
    } catch (error) {
        showAlert('queueContent', `❌ Lỗi: ${error.message}`, 'error');
    }
}

// Form handlers
document.getElementById('addForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const url = document.getElementById('urlInput').value.trim();
    const selectedCategory = document.getElementById('categorySelect').value;
    const newCategory = document.getElementById('newCategoryInput').value.trim();
    const category = newCategory || selectedCategory;
    
    if (!url) {
        showAlert('addAlert', '❌ Vui lòng nhập URL', 'error');
        return;
    }
    
    if (!url.includes('xiaohongshu.com') && !url.includes('xhslink.com')) {
        showAlert('addAlert', '❌ URL không hợp lệ', 'error');
        return;
    }
    
    try {
        const result = await apiCall('/add', {
            method: 'POST',
            body: JSON.stringify({ url, category })
        });
        
        if (result.success) {
            showAlert('addAlert', `✅ ${result.message}`, 'success');
            document.getElementById('addForm').reset();
            await loadCategories();
        } else {
            showAlert('addAlert', `⚠️ ${result.message}`, 'error');
        }
    } catch (error) {
        showAlert('addAlert', `❌ Lỗi: ${error.message}`, 'error');
    }
});

document.getElementById('configForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const downloadPath = document.getElementById('downloadPath').value.trim();
    const delaySeconds = parseInt(document.getElementById('delaySeconds').value);
    
    if (!downloadPath) {
        showAlert('configAlert', '❌ Vui lòng nhập thư mục lưu', 'error');
        return;
    }
    
    if (!delaySeconds || delaySeconds < 30) {
        showAlert('configAlert', '❌ Delay phải >= 30 giây', 'error');
        return;
    }
    
    try {
        await apiCall('/config', {
            method: 'POST',
            body: JSON.stringify({
                download_path: downloadPath,
                delay_seconds: delaySeconds
            })
        });
        
        showAlert('configAlert', '✅ Đã lưu cài đặt', 'success');
    } catch (error) {
        showAlert('configAlert', `❌ Lỗi: ${error.message}`, 'error');
    }
});

// Auto refresh
setInterval(async () => {
    if (document.querySelector('.tab[data-tab="queue"]').classList.contains('active')) {
        await loadQueue();
    }
}, 10000);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadQueue();
    loadCategories();
});