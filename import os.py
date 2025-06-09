import os
import re
import pandas as pd

def save_to_excel(results, search_bar_keyword, filter_keywords_input, min_play_num):
    if not results:
        print("没有数据，无需保存。")
        return None

    filename_search = re.sub(r'[\\/:*?"<>|]', "", search_bar_keyword)
    filename_filter = re.sub(r'[\\/:*?"<>|]', "", filter_keywords_input.replace("+", "_"))
    filename = f"{filename_search}-{filename_filter}-{min_play_num}.xlsx"

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    save_path = os.path.join(desktop_path, filename)

    df = pd.DataFrame(results)
    df.to_excel(save_path, index=False)
    print(f"数据已保存到：{save_path}")
    return save_path
