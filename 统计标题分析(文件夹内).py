import pandas as pd
import jieba
import matplotlib.pyplot as plt
from collections import defaultdict
import os

def parse_play_num(play_str):
    try:
        if not isinstance(play_str, str):
            return 0
        play_str = play_str.replace("播放", "").replace("观看", "").strip()
        if "万" in play_str:
            return int(float(play_str.replace("万", "")) * 10000)
        else:
            return int(''.join(filter(str.isdigit, play_str)))
    except:
        return 0

def list_excel_files(folder):
    files = [f for f in os.listdir(folder) if f.endswith(('.xls', '.xlsx'))]
    return files

def analyze_and_plot(file_path):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"读取Excel失败：{e}")
        return

    required_columns = {"标题", "链接", "播放量"}
    if not required_columns.issubset(set(df.columns)):
        print(f"Excel中必须包含列: {required_columns}")
        return

    df["播放量数值"] = df["播放量"].apply(parse_play_num)

    # 播放量区间分布
    bins = [0, 10000, 50000, 100000, float('inf')]
    labels = ['0-1万', '1万-5万', '5万-10万', '10万以上']
    df['播放量区间'] = pd.cut(df['播放量数值'], bins=bins, labels=labels, right=False)
    distribution = df['播放量区间'].value_counts().sort_index()

    # 关键词分析
    word_data = defaultdict(list)
    for idx, title in enumerate(df["标题"]):
        if not isinstance(title, str):
            continue
        words = set(jieba.lcut(title))
        play_val = df.loc[idx, "播放量数值"]
        for w in words:
            if w.strip():
                word_data[w].append(play_val)

    word_stats = []
    for w, plays in word_data.items():
        count = len(plays)
        avg_p = sum(plays) / count if count > 0 else 0
        word_stats.append((w, count, avg_p))

    word_stats.sort(key=lambda x: x[2], reverse=True)
    top_words = word_stats[:20]

    # 画播放量区间分布条形图
    plt.figure(figsize=(10, 5))
    plt.bar(distribution.index.astype(str), distribution.values, color='skyblue')
    plt.title("播放量区间分布")
    plt.xlabel("播放量区间")
    plt.ylabel("视频数量")
    for i, v in enumerate(distribution.values):
        plt.text(i, v + max(distribution.values)*0.01, str(v), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

    # 画标题关键词平均播放量柱状图
    words = [w for w, _, _ in top_words]
    avg_plays = [a for _, _, a in top_words]

    plt.figure(figsize=(14, 7))
    bars = plt.bar(words, avg_plays, color='salmon')
    plt.title("标题关键词与平均播放量（Top 20）")
    plt.xlabel("关键词")
    plt.ylabel("平均播放量")
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height * 1.01, f'{int(height):,}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def main():
    folder = os.getcwd()
    files = list_excel_files(folder)
    if not files:
        print("当前目录没有找到任何 Excel 文件。")
        return

    print("当前目录找到以下 Excel 文件：")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    while True:
        choice = input(f"请输入要分析的文件编号 (1-{len(files)}), 或输入q退出: ").strip()
        if choice.lower() == 'q':
            print("退出程序。")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            selected_file = files[int(choice)-1]
            print(f"开始分析文件: {selected_file}")
            analyze_and_plot(os.path.join(folder, selected_file))
            break
        else:
            print("输入无效，请重新输入。")

if __name__ == "__main__":
    main()
