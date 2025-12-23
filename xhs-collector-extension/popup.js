const API_BASE = 'http://localhost:8080/api';

// Hiển thị status
function showStatus(msg, type = 'info') {
  const el = document.getElementById('status');
  el.textContent = msg;
  el.className = `status ${type}`;
  el.style.display = 'block';
  setTimeout(() => el.style.display = 'none', 3000);
}

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
  tab.onclick = () => {
    const tabName = tab.dataset.tab;
    
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.remove('active');
    });
    document.getElementById(tabName + 'Tab').classList.add('active');
    
    if (tabName === 'config') {
      loadConfig();
    }
  };
});

// Load config
async function loadConfig() {
  try {
    const res = await fetch(`${API_BASE}/config`);
    const config = await res.json();
    
    document.getElementById('downloadPath').value = config.download_path || '/app/Volume/Download';
    document.getElementById('delaySeconds').value = config.delay_seconds || 120;
  } catch (e) {
    showStatus('❌ Không thể tải config', 'error');
  }
}

// Save config
document.getElementById('saveConfigBtn').onclick = async () => {
  const downloadPath = document.getElementById('downloadPath').value.trim();
  const delaySeconds = parseInt(document.getElementById('delaySeconds').value);
  
  if (!downloadPath) {
    showStatus('❌ Vui lòng nhập thư mục lưu', 'error');
    return;
  }
  
  if (!delaySeconds || delaySeconds < 30) {
    showStatus('❌ Delay phải >= 30 giây', 'error');
    return;
  }
  
  try {
    const res = await fetch(`${API_BASE}/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        download_path: downloadPath,
        delay_seconds: delaySeconds
      })
    });
    
    if (res.ok) {
      showStatus('✅ Đã lưu cài đặt', 'success');
    } else {
      showStatus('❌ Lỗi lưu cài đặt', 'error');
    }
  } catch (e) {
    showStatus('❌ Không thể kết nối server', 'error');
  }
};

// Load queue từ server
async function loadQueue() {
  try {
    const res = await fetch(`${API_BASE}/queue`);
    return await res.json();
  } catch (e) {
    return { items: [], stats: { pending: 0, done: 0, error: 0 } };
  }
}

// Load categories
async function loadCategories() {
  try {
    const res = await fetch(`${API_BASE}/categories`);
    const categories = await res.json();
    const list = document.getElementById('categoryList');
    
    if (categories.length === 0) {
      list.innerHTML = '<div class="empty">Chưa có category nào</div>';
      return;
    }
    
    list.innerHTML = categories.map(cat => `
      <div class="queue-item">
        <span class="url">📁 ${cat.name} (${cat.count})</span>
        <span class="remove" onclick="document.getElementById('categoryInput').value='${cat.name}'">📝</span>
      </div>
    `).join('');
  } catch (e) {
    document.getElementById('categoryList').innerHTML = '<div class="empty">Lỗi tải categories</div>';
  }
}

// Render queue list
async function renderQueue() {
  const data = await loadQueue();
  const list = document.getElementById('queueList');
  
  document.getElementById('pendingCount').textContent = data.stats.pending;
  document.getElementById('doneCount').textContent = data.stats.done;
  document.getElementById('errorCount').textContent = data.stats.error;
  
  const pending = data.items.filter(i => i.status === 'pending');
  
  if (pending.length === 0) {
    list.innerHTML = '<div class="empty">Không có link pending</div>';
  } else {
    list.innerHTML = pending.slice(0, 15).map(item => `
      <div class="queue-item">
        <span class="url" title="${item.url}">📁${item.category || 'default'} ${item.url.substring(0, 25)}...</span>
        <span class="remove" data-id="${item.id}">✕</span>
      </div>
    `).join('');
    
    // Add remove handlers
    list.querySelectorAll('.remove').forEach(btn => {
      btn.onclick = async () => {
        await fetch(`${API_BASE}/queue/${btn.dataset.id}`, { method: 'DELETE' });
        renderQueue();
      };
    });
  }
  
  // Load categories
  loadCategories();
}

// Kiểm tra URL hợp lệ
function isValidXhsUrl(url) {
  return url && (
    url.includes('xiaohongshu.com/explore/') ||
    url.includes('xiaohongshu.com/discovery/item/') ||
    url.includes('xhslink.com/')
  );
}

// Thêm link
document.getElementById('addBtn').onclick = async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;
  const category = document.getElementById('categoryInput').value.trim() || 'default';
  
  if (!isValidXhsUrl(url)) {
    showStatus('❌ Không phải link XHS hợp lệ', 'error');
    return;
  }
  
  try {
    const res = await fetch(`${API_BASE}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, category })
    });
    const data = await res.json();
    
    if (data.success) {
      showStatus(`✅ ${data.message}`, 'success');
    } else {
      showStatus(`⚠️ ${data.message}`, 'error');
    }
    renderQueue();
  } catch (e) {
    showStatus('❌ Không thể kết nối server', 'error');
  }
};

// Xóa tất cả pending
document.getElementById('clearBtn').onclick = async () => {
  try {
    await fetch(`${API_BASE}/queue`, { method: 'DELETE' });
    renderQueue();
    showStatus('🗑️ Đã xóa pending', 'info');
  } catch (e) {
    showStatus('❌ Lỗi kết nối', 'error');
  }
};

// Refresh
document.getElementById('refreshBtn').onclick = () => {
  renderQueue();
  showStatus('🔄 Đã refresh', 'info');
};

// Init
renderQueue();
// Auto refresh mỗi 10s
setInterval(renderQueue, 10000);
