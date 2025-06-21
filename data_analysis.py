# data_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from config import PLOT_FILE, RESULTS_FOLDER
import os


def analyze_and_visualize(df):
    """分析数据并生成可视化图表"""
    if df.empty:
        print("没有数据可供分析")
        return

    # 确保结果目录存在
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    # 修复1: 将年份转换为整数类型
    try:
        # 尝试将年份转换为整数
        df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)

        # 过滤掉无效年份（1900年之前或未来年份）
        current_year = pd.Timestamp.now().year
        df = df[(df['year'] > 1900) & (df['year'] <= current_year + 1)]
    except Exception as e:
        print(f"年份转换错误: {e}")
        return

    # 按年份统计电影数量
    year_counts = df['year'].value_counts().sort_index()

    # 解决中文乱码问题
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 创建图表
    plt.figure(figsize=(12, 6))

    # 使用更清晰的线条样式
    year_counts.plot(kind='line', marker='o', color='#e74c3c',
                     linewidth=2, markersize=8, markeredgecolor='white')

    # 添加标题和标签 - 优化标题内容
    plt.title('豆瓣电影Top250年度分布分析', fontsize=16, pad=20)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('电影数量', fontsize=12)

    # 添加网格线
    plt.grid(True, linestyle='--', alpha=0.5)

    # 设置x轴范围
    min_year = max(1950, year_counts.index.min() - 1) if not year_counts.empty else 1950
    max_year = min(current_year, year_counts.index.max() + 1) if not year_counts.empty else current_year

    # 确保有足够的年份范围
    if max_year - min_year < 5:
        min_year = min_year - 2
        max_year = max_year + 2

    plt.xlim(min_year, max_year)

    # 添加数据标签 - 优化显示位置
    for x, y in zip(year_counts.index, year_counts.values):
        plt.text(x, y + 0.3, str(y), ha='center', va='bottom',
                 fontsize=10, fontweight='bold', color='#2c3e50')

    # 添加峰值标注
    if not year_counts.empty:
        peak_year = year_counts.idxmax()
        peak_count = year_counts.max()
        plt.annotate(f'峰值: {peak_year}年 ({peak_count}部)',
                     xy=(peak_year, peak_count),
                     xytext=(peak_year, peak_count + 1.5),
                     arrowprops=dict(facecolor='#3498db', shrink=0.05),
                     fontsize=11,
                     ha='center')

    # 添加数据来源标注
    plt.figtext(0.5, 0.01, '数据来源: 豆瓣电影 Top250',
                ha='center', fontsize=9, color='#7f8c8d', alpha=0.7)

    # 保存图表
    plt.tight_layout()
    plt.savefig(PLOT_FILE, dpi=300, bbox_inches='tight')
    print(f"年度分布图已保存到: {PLOT_FILE}")

    # 显示统计信息
    print("\n数据分析结果:")

    if not year_counts.empty:
        print(f"最早电影年份: {year_counts.index.min()}")
        print(f"最新电影年份: {year_counts.index.max()}")
        print(f"电影数量最多的年份: {peak_year}年 ({peak_count}部)")
    else:
        print("没有有效的年份数据")

    print(f"电影总数量: {len(df)}部")

    # 返回统计结果
    return {
        'earliest_year': year_counts.index.min() if not year_counts.empty else 0,
        'latest_year': year_counts.index.max() if not year_counts.empty else 0,
        'peak_year': peak_year if not year_counts.empty else 0,
        'peak_count': peak_count if not year_counts.empty else 0,
        'total_movies': len(df)
    }