import tkinter as tk
from tkinter import simpledialog, messagebox

def get_search_and_filter():
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

def get_play_and_pages():
    root = tk.Tk()
    root.withdraw()
    play_and_page = simpledialog.askstring(
        "播放量阈值和抓取页数",
        "请输入播放量最低值和抓取页数，用逗号分隔\n示例：10000,5\n默认5页，播放量最低0"
    )
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
    return min_play_num, max_pages
