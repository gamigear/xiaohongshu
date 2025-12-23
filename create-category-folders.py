#!/usr/bin/env python3
"""
Script tạo thư mục con theo category trong Docker container
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://neondb_owner:npg_JSZwFQ0K8rXI@ep-soft-brook-a1a086es-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
BASE_PATH = "./XHS-Downloader/Volume/Download"

def get_categories():
    """Lấy danh sách categories từ DB"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM xhs_queue WHERE category IS NOT NULL")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [r["category"] for r in rows]

def create_folders():
    """Tạo thư mục cho mỗi category"""
    categories = get_categories()
    
    for category in categories:
        folder_path = os.path.join(BASE_PATH, category)
        os.makedirs(folder_path, exist_ok=True)
        print(f"✅ Created: {folder_path}")
    
    print(f"🎉 Created {len(categories)} category folders")

if __name__ == "__main__":
    create_folders()