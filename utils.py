# utils.py
import os
import re
import time
import random
import requests
from config import IMG_FOLDER, DATA_FOLDER, RESULTS_FOLDER, MAX_RETRIES, DELAY_RANGE, HEADERS


def create_directories():
    """创建必要的目录结构"""
    for folder in [IMG_FOLDER, DATA_FOLDER, RESULTS_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"创建目录: {folder}")


def safe_filename(title):
    """创建安全的文件名（替换非法字符）"""
    return re.sub(r'[\\/*?:"<>|]', "", title)


import os
import hashlib
from datetime import datetime


def get_page_with_retry(url, max_retries=MAX_RETRIES):
    """带重试机制的页面获取函数，默认保存HTML内容到文件"""
    # 创建HTML保存目录
    html_dir = "html_pages"
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)

    # 生成文件名（时间戳 + URL哈希）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
    filename = f"{timestamp}_{url_hash}.html"
    filepath = os.path.join(html_dir, filename)

    for attempt in range(max_retries):
        try:
            # 添加随机延迟
            time.sleep(random.uniform(*DELAY_RANGE))

            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            # 检查反爬机制
            if "检测到有异常请求" in response.text:
                print(f"触发反爬机制: {url}")
                time.sleep(5)
                continue

            html_content = response.text

            # 总是保存HTML到文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"已保存HTML内容到: {filepath}")

            return html_content

        except requests.exceptions.RequestException as e:
            print(f"请求失败 ({attempt + 1}/{max_retries}): {e}")
            time.sleep(2)

    print(f"无法获取页面: {url}")

    # 即使失败也创建空文件标记
    open(filepath, 'w', encoding='utf-8').close()
    print(f"创建空文件标记失败请求: {filepath}")

    return None

def download_image(img_url, filename):
    """下载并保存电影海报"""
    if not img_url:
        return False

    try:
        response = requests.get(img_url, headers=HEADERS, stream=True, timeout=10)
        response.raise_for_status()

        # 保存图片
        img_path = os.path.join(IMG_FOLDER, filename)
        with open(img_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"下载图片失败: {img_url} - {e}")
        return False