# config.py
import os

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_FOLDER = os.path.join(BASE_DIR, "film_img")
DATA_FOLDER = os.path.join(BASE_DIR, "data")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")

# 豆瓣爬虫配置
BASE_URL = "https://movie.douban.com/top250"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive'
}
DELAY_RANGE = (1, 3)  # 随机延迟范围（秒）
MAX_WORKERS = 4       # 最大线程数
MAX_RETRIES = 3       # 最大重试次数  # 确保这个变量存在

# 文件路径配置
CSV_FILE = os.path.join(DATA_FOLDER, "douban_top250_chinese_movies.csv")
PLOT_FILE = os.path.join(RESULTS_FOLDER, "movie_count_by_year.png")