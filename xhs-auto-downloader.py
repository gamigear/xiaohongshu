#!/usr/bin/env python3
"""
XHS Auto Downloader - Tự động tải link từ file với delay 2 phút
Sử dụng: python xhs-auto-downloader.py [file_links.txt]
"""

import requests
import time
import sys
import os
from datetime import datetime

API_URL = "http://localhost:5556/xhs/detail"
DELAY_SECONDS = 120  # 2 phút
LINKS_FILE = "xhs_links.txt"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def download_post(url):
    """Tải một post từ XHS"""
    try:
        response = requests.post(
            API_URL,
            json={"url": url.strip(), "download": True},
            timeout=60
        )
        data = response.json()
        
        if data.get("data"):
            title = data["data"].get("作品标题", "Untitled")
            author = data["data"].get("作者昵称", "Unknown")
            post_type = data["data"].get("作品类型", "Unknown")
            return True, f"{title} - {author} ({post_type})"
        else:
            return False, data.get("message", "Unknown error")
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối API. Đảm bảo Docker đang chạy!"
    except Exception as e:
        return False, str(e)

def main():
    links_file = sys.argv[1] if len(sys.argv) > 1 else LINKS_FILE
    
    # Tạo file mẫu nếu chưa có
    if not os.path.exists(links_file):
        with open(links_file, "w") as f:
            f.write("# Thêm link XHS vào đây, mỗi link một dòng\n")
            f.write("# Ví dụ: https://www.xiaohongshu.com/explore/xxx?xsec_token=xxx\n")
        log(f"Đã tạo file {links_file}. Thêm link vào file và chạy lại!")
        return
    
    # Đọc links
    with open(links_file, "r") as f:
        links = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    if not links:
        log("Không có link nào trong file!")
        return
    
    log(f"Tìm thấy {len(links)} link")
    log(f"Delay giữa mỗi lần tải: {DELAY_SECONDS}s ({DELAY_SECONDS//60} phút)")
    log("-" * 50)
    
    success_count = 0
    failed_links = []
    
    for i, url in enumerate(links, 1):
        log(f"[{i}/{len(links)}] Đang tải: {url[:60]}...")
        
        ok, msg = download_post(url)
        
        if ok:
            log(f"✅ Thành công: {msg}")
            success_count += 1
        else:
            log(f"❌ Lỗi: {msg}")
            failed_links.append(url)
        
        # Delay nếu còn link tiếp theo
        if i < len(links):
            log(f"⏳ Chờ {DELAY_SECONDS}s trước khi tải tiếp...")
            for remaining in range(DELAY_SECONDS, 0, -10):
                time.sleep(10)
                if remaining > 10:
                    print(f"   Còn {remaining-10}s...", end="\r")
            print(" " * 30, end="\r")
    
    log("-" * 50)
    log(f"🎉 Hoàn thành! Thành công: {success_count}/{len(links)}")
    
    # Lưu lại các link lỗi
    if failed_links:
        failed_file = "xhs_failed.txt"
        with open(failed_file, "w") as f:
            f.write("\n".join(failed_links))
        log(f"⚠️ Các link lỗi đã lưu vào {failed_file}")
    
    # Xóa file links sau khi hoàn thành
    if success_count == len(links):
        os.rename(links_file, links_file + ".done")
        log(f"📁 File đã đổi tên thành {links_file}.done")

if __name__ == "__main__":
    main()
