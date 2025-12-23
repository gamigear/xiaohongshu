#!/usr/bin/env python3
"""
XHS Download Worker - Tự động lấy link từ DB và tải với delay
"""

import os
import sys
import time
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
XHS_API_URL = os.getenv("XHS_API_URL", "http://localhost:5556/xhs/detail")
DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", 120))

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def get_next_pending():
    """Lấy link pending tiếp theo"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, url, category FROM xhs_queue 
        WHERE status = 'pending' 
        ORDER BY created_at ASC 
        LIMIT 1
    """)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return dict(row) if row else None

def update_status(id, status, title=None, author=None, post_type=None, error_msg=None):
    """Cập nhật trạng thái"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE xhs_queue 
        SET status = %s, title = %s, author = %s, post_type = %s, 
            error_msg = %s, downloaded_at = CASE WHEN %s = 'done' THEN NOW() ELSE NULL END
        WHERE id = %s
    """, (status, title, author, post_type, error_msg, status, id))
    conn.commit()
    cur.close()
    conn.close()

def download_post(url, category="default"):
    """Gọi XHS API để tải với thư mục con"""
    try:
        # Tạo thư mục con theo category
        download_data = {
            "url": url, 
            "download": True
        }
        
        # Gọi API với folder_name custom nếu cần
        response = requests.post(
            XHS_API_URL,
            json=download_data,
            timeout=120
        )
        data = response.json()
        
        if data.get("data"):
            return {
                "success": True,
                "title": data["data"].get("作品标题"),
                "author": data["data"].get("作者昵称"),
                "post_type": data["data"].get("作品类型"),
                "category": category
            }
        else:
            return {"success": False, "error": data.get("message", "Unknown error")}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Không thể kết nối XHS API"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_pending_count():
    """Đếm số pending"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM xhs_queue WHERE status = 'pending'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row["cnt"]

def init_db():
    """Tạo bảng nếu chưa có"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS xhs_queue (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL UNIQUE,
            status VARCHAR(20) DEFAULT 'pending',
            title TEXT,
            author TEXT,
            post_type VARCHAR(20),
            category VARCHAR(50) DEFAULT 'default',
            error_msg TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            downloaded_at TIMESTAMP
        )
    """)
    # Thêm cột category nếu chưa có (cho DB cũ)
    cur.execute("""
        ALTER TABLE xhs_queue 
        ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'default'
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_config():
    """Lấy config từ database"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM xhs_config")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    config = {r["key"]: r["value"] for r in rows}
    return {
        "delay_seconds": int(config.get("delay_seconds", 120)),
        "download_path": config.get("download_path", "/app/Volume/Download")
    }

def main():
    log("🚀 XHS Download Worker started")
    log(f"📡 XHS API: {XHS_API_URL}")
    
    # Đảm bảo bảng tồn tại
    init_db()
    log("✅ Database ready")
    
    while True:
        # Đọc config mới nhất
        config = get_config()
        delay_seconds = config["delay_seconds"]
        
        log(f"⏱️  Current delay: {delay_seconds}s ({delay_seconds//60} phút)")
        
        item = get_next_pending()
        
        if not item:
            log("💤 Không có link pending. Chờ 30s...")
            time.sleep(30)
            continue
        
        pending = get_pending_count()
        category = item.get('category', 'default')
        log(f"📥 [{pending} pending] [{category}] Đang tải: {item['url'][:50]}...")
        
        result = download_post(item["url"], category)
        
        if result["success"]:
            update_status(
                item["id"], "done",
                title=result["title"],
                author=result["author"],
                post_type=result["post_type"]
            )
            log(f"✅ Thành công [{category}]: {result['title']} - {result['author']}")
        else:
            update_status(item["id"], "error", error_msg=result["error"])
            log(f"❌ Lỗi [{category}]: {result['error']}")
        
        # Check còn pending không
        if get_pending_count() > 0:
            log(f"⏳ Chờ {delay_seconds}s trước khi tải tiếp...")
            for remaining in range(delay_seconds, 0, -10):
                time.sleep(10)
                if remaining > 10:
                    print(f"   Còn {remaining-10}s...", end="\r")
            print(" " * 30, end="\r")

if __name__ == "__main__":
    main()
