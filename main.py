# main.py
import pandas as pd
from crawler import crawl_douban_top250
from data_analysis import analyze_and_visualize
from config import CSV_FILE, DATA_FOLDER
import os


def main():
    print("豆瓣电影 Top250 数据爬取与分析系统")
    print("=" * 50)

    # 检查是否已存在数据文件
    if os.path.exists(CSV_FILE):
        print(f"检测到已有数据文件: {CSV_FILE}")
        df = pd.read_csv(CSV_FILE)
        print(f"从文件加载 {len(df)} 条电影记录")
        print("提示：如需重新爬取，请删除现有数据文件")
    else:
        print("未找到现有数据文件，开始爬取数据...")
        df = crawl_douban_top250()

    # 进行数据分析和可视化
    print("\n开始数据分析...")
    stats = analyze_and_visualize(df)

    # 打印统计摘要
    print("\n" + "=" * 50)
    print("数据摘要:")
    print(f"最早电影年份: {stats['earliest_year']}")
    print(f"最新电影年份: {stats['latest_year']}")
    print(f"电影数量最多的年份: {stats['peak_year']}年 ({stats['peak_count']}部)")
    print(f"电影总数量: {stats['total_movies']}部")
    print("=" * 50)

    print("\n程序执行完成！")
    print(f"电影海报保存在: film_img/")
    print(f"数据文件保存在: data/")
    print(f"分析结果保存在: results/")


if __name__ == "__main__":
    main()