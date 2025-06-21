# crawler.py
from bs4 import BeautifulSoup
import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import BASE_URL, MAX_WORKERS, CSV_FILE
from utils import create_directories, safe_filename, get_page_with_retry, download_image

from bs4 import BeautifulSoup


def parse_movie_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    movies = []

    for item in soup.select('ol.grid_view li .item'):
        # 电影标题
        title = item.select_one('.hd .title:first-child').text.strip()

        # 海报URL
        poster = item.select_one('.pic img')['src']

        # 提取年份和地区
        bd = item.select_one('.bd p')
        if bd:
            # 找到所有的文本节点
            contents = bd.contents

            # 寻找包含年份/地区信息的文本节点（在<br>标签之后）
            info_text = ""
            found_br = False

            for content in contents:
                if content.name == 'br':
                    found_br = True
                elif found_br and isinstance(content, str):
                    info_text = content.strip()
                    break

            if info_text:
                # 分割信息部分
                parts = info_text.split('/')
                if len(parts) >= 2:
                    year = parts[0].strip()
                    region = parts[1].strip()
                else:
                    year = ""
                    region = ""
            else:
                year = ""
                region = ""
        else:
            year = ""
            region = ""

        movies.append({
            'title': title,
            'year': year,
            'region': region,
            'poster': poster
        })

    return movies

def crawl_douban_top250():
    """爬取豆瓣Top250电影数据"""
    create_directories()
    all_movies = []
    page_urls = [f"{BASE_URL}?start={i * 25}" for i in range(10)]

    print("开始爬取豆瓣Top250电影数据...")

    # 使用线程池提高效率
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {
            executor.submit(get_page_with_retry, url): url
            for url in page_urls
        }

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                html = future.result()
                if html:
                    movies = parse_movie_info(html)
                    all_movies.extend(movies)
                    print(f"成功解析页面: {url}, 获取电影数: {len(movies)}")
            except Exception as e:
                print(f"处理页面失败 {url}: {e}")

    print(f"共获取 {len(all_movies)} 部国内中文电影")

    # 保存数据到CSV
    df = pd.DataFrame(all_movies)
    df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
    print(f"电影数据已保存到: {CSV_FILE}")

    # 下载电影海报
    print("开始下载电影海报...")
    img_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for _, row in df.iterrows():
            filename = f"{safe_filename(row['title'])}.jpg"
            futures.append(executor.submit(
                download_image,
                row['poster'],
                filename
            ))

        for future in as_completed(futures):
            if future.result():
                img_count += 1

    print(f"成功下载 {img_count}/{len(df)} 张电影海报")

    return df