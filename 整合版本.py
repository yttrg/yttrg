import re
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import simpledialog, messagebox

def parse_play_count(play_str):
    try:
        if not play_str or "播放量" in play_str or "获取失败" in play_str:
            return -1
        play_str = play_str.replace("播放", "").replace("观看", "").strip()
        match = re.match(r"([\d\.]+)(万)?", play_str)
        if match:
            num = float(match.group(1))
            if match.group(2):
                return int(num * 10000)
            else:
                return int(num)
        num = int(re.sub(r"[^\d]", "", play_str))
        return num
    except Exception:
        return -1

def extract_play(card):
    try:
        play = card.find_element(By.CSS_SELECTOR, ".bili-video-card__stats--item:nth-child(1)").text.strip()
        if play:
            return play
    except:
        pass
    try:
        spans = card.find_elements(By.CSS_SELECTOR, "span")
        for span in spans:
            txt = span.text.strip()
            if any(k in txt for k in ["万", "次", "观看"]):
                return txt
    except:
        pass
    return "（播放量获取失败）"

def get_two_inputs():
    root = tk.Tk()
    root.title("请输入关键词")
    root.geometry("400x150")
    root.resizable(False, False)

    tk.Label(root, text="搜索栏关键词（用于B站搜索页）:").pack(pady=(10, 0))
    search_bar_entry = tk.Entry(root, width=50)
    search_bar_entry.pack()

    tk.Label(root, text="检索关键词（多个用 + 号连接）:").pack(pady=(10, 0))
    filter_keywords_entry = tk.Entry(root, width=50)
    filter_keywords_entry.pack()

    result = {}

    def on_submit():
        search_val = search_bar_entry.get().strip()
        filter_val = filter_keywords_entry.get().strip()
        if not search_val:
            messagebox.showwarning("警告", "搜索栏关键词不能为空")
            return
        if not filter_val:
            messagebox.showwarning("警告", "检索关键词不能为空")
            return
        result['search'] = search_val
        result['filter'] = filter_val
        root.destroy()

    submit_btn = tk.Button(root, text="确定", command=on_submit)
    submit_btn.pack(pady=10)

    root.mainloop()
    return result.get('search', None), result.get('filter', None)

def main():
    search_bar_keyword, filter_keywords_input = get_two_inputs()
    if not search_bar_keyword or not filter_keywords_input:
        print("未输入关键词，程序退出。")
        return

    filter_keywords = [k.strip() for k in filter_keywords_input.split("+") if k.strip()]

    root2 = tk.Tk()
    root2.withdraw()
    play_and_page = simpledialog.askstring("播放量阈值和抓取页数",
                                           "请输入播放量最低值和抓取页数，用逗号分隔\n示例：10000,5\n默认5页，播放量最低0")
    if play_and_page:
        parts = play_and_page.split(",")
        try:
            min_play_num = int(parts[0])
        except:
            min_play_num = 0
        try:
            max_pages = int(parts[1]) if len(parts) > 1 else 5
        except:
            max_pages = 5
    else:
        min_play_num = 0
        max_pages = 5

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    results = []
    for page in range(1, max_pages + 1):
        url = f"https://search.bilibili.com/video?keyword={search_bar_keyword}&page={page}"
        print(f"正在抓取第 {page} 页：{url}")
        driver.get(url)
        time.sleep(5)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.bili-video-card")
        print(f"本页找到视频卡片数：{len(cards)}")

        for i, card in enumerate(cards, 1):
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "h3")
                title = title_elem.get_attribute("title").strip()

                if not any(k in title for k in filter_keywords):
                    continue

                link_elem = card.find_element(By.CSS_SELECTOR, "a")
                href = link_elem.get_attribute("href")
                if "cheese" in href:
                    continue

                play = extract_play(card)
                play_num = parse_play_count(play)
                if play_num >= min_play_num:
                    results.append({"标题": title, "链接": href, "播放量": play})

                    print(f"第{page}页，第{i}个视频")
                    print(f"标题: {title}")
                    print(f"链接: {href}")
                    print(f"播放量: {play}")
                    print("-" * 40)

            except Exception as e:
                print(f"第{page}页，第{i}个视频处理异常，跳过")
                print(e)
                print("-" * 40)

    driver.quit()

    if not results:
        print(f"没有符合条件的视频，关键词过滤后播放量≥{min_play_num}的视频未找到。")
        return

    # 构造文件名，过滤特殊字符
    filename_search = re.sub(r'[\\/:*?"<>|]', "", search_bar_keyword)
    filename_filter = re.sub(r'[\\/:*?"<>|]', "", filter_keywords_input.replace("+", "_"))
    filename = f"{filename_search}-{filename_filter}-{min_play_num}.xlsx"

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    save_path = os.path.join(desktop_path, filename)

    df = pd.DataFrame(results)
    df.to_excel(save_path, index=False)
    print(f"数据已保存到：{save_path}")

if __name__ == "__main__":
    main()
