#!/usr/bin/env python3
"""
XHS Queue Server - API để lưu link vào PostgreSQL
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="XHS Queue Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serve web interface"""
    return FileResponse("static/index.html")

@app.get("/dashboard")
async def dashboard():
    """Serve dashboard"""
    return FileResponse("static/dashboard.html")

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

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

class LinkRequest(BaseModel):
    url: str
    category: str = "default"

class LinkResponse(BaseModel):
    success: bool
    message: str
    id: int = None

class ConfigRequest(BaseModel):
    download_path: str = None
    delay_seconds: int = None

def init_config_table():
    """Tạo bảng config"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS xhs_config (
            key VARCHAR(50) PRIMARY KEY,
            value TEXT
        )
    """)
    # Default values
    cur.execute("""
        INSERT INTO xhs_config (key, value) VALUES ('download_path', '/app/Volume/Download')
        ON CONFLICT (key) DO NOTHING
    """)
    cur.execute("""
        INSERT INTO xhs_config (key, value) VALUES ('delay_seconds', '120')
        ON CONFLICT (key) DO NOTHING
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()
    init_config_table()

@app.post("/api/add", response_model=LinkResponse)
async def add_link(req: LinkRequest):
    """Thêm link vào queue"""
    url = req.url.strip()
    category = req.category.strip() or "default"
    
    if not any(x in url for x in ["xiaohongshu.com/explore/", "xiaohongshu.com/discovery/", "xhslink.com/"]):
        raise HTTPException(400, "URL không hợp lệ")
    
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO xhs_queue (url, category) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING RETURNING id",
            (url, category)
        )
        result = cur.fetchone()
        conn.commit()
        
        if result:
            return LinkResponse(success=True, message=f"Đã thêm vào queue [{category}]", id=result["id"])
        else:
            return LinkResponse(success=False, message="Link đã tồn tại")
    finally:
        cur.close()
        conn.close()

@app.get("/api/queue")
async def get_queue():
    """Lấy danh sách queue"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, url, status, title, author, post_type, category, error_msg, 
               created_at, downloaded_at 
        FROM xhs_queue 
        ORDER BY created_at DESC 
        LIMIT 100
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return {
        "items": [dict(r) for r in rows],
        "stats": {
            "pending": sum(1 for r in rows if r["status"] == "pending"),
            "done": sum(1 for r in rows if r["status"] == "done"),
            "error": sum(1 for r in rows if r["status"] == "error")
        }
    }

@app.get("/api/categories")
async def get_categories():
    """Lấy danh sách categories"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT category, COUNT(*) as count
        FROM xhs_queue 
        WHERE category IS NOT NULL
        GROUP BY category 
        ORDER BY category
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [{"name": r["category"], "count": r["count"]} for r in rows]

@app.delete("/api/queue/{id}")
async def delete_item(id: int):
    """Xóa item khỏi queue"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM xhs_queue WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"success": True}

@app.delete("/api/queue")
async def clear_queue():
    """Xóa tất cả pending"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM xhs_queue WHERE status = 'pending'")
    conn.commit()
    cur.close()
    conn.close()
    return {"success": True}

@app.get("/api/config")
async def get_config():
    """Lấy config"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM xhs_config")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {r["key"]: r["value"] for r in rows}

@app.post("/api/config")
async def update_config(req: ConfigRequest):
    """Cập nhật config"""
    conn = get_db()
    cur = conn.cursor()
    
    if req.download_path:
        cur.execute(
            "UPDATE xhs_config SET value = %s WHERE key = 'download_path'",
            (req.download_path,)
        )
    if req.delay_seconds:
        cur.execute(
            "UPDATE xhs_config SET value = %s WHERE key = 'delay_seconds'",
            (str(req.delay_seconds),)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
