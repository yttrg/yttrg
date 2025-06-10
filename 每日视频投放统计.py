import pandas as pd
from datetime import datetime

# === 1. 配置路径 ===
excel_path = r"C:\Users\UserComputer\Desktop\崔震林投放表.xlsx"
output_txt = r"C:\Users\UserComputer\Desktop\投放统计.txt"

# === 2. 打开 Excel 中的第二个工作表（视频投放）===
xls = pd.ExcelFile(excel_path)
if len(xls.sheet_names) < 2:
    raise ValueError("Excel 文件中没有第二个子表，请检查文件格式。")

# 确保是“视频投放”表（你也可以直接用 sheet_name="视频投放"）
df = xls.parse(sheet_name=1)  # 第二个工作表索引为1

# === 3. 获取今天日期字符串（比如 6.07）===
today_str = datetime.now().strftime('%#m.%d')  # Windows 用户用这个
# 如果你在 Linux/MacOS，用下面这一行：
# today_str = datetime.now().strftime('%-m.%d')

# === 4. 获取列名列表，确保可读性 ===
df.columns = df.columns.map(lambda x: str(x).strip())
columns_list = df.columns.tolist()

# 检查列数是否够用
if len(columns_list) < 11:
    raise ValueError("子表中列数不足11列，请检查表结构。")

# 获取 B列 和 K列 的列名（按位置）
b_col = columns_list[1]   # 第2列是 B列
k_col = columns_list[10]  # 第11列是 K列

# === 5. 按 B 列值是否等于今日日期筛选数据 ===
filtered_df = df[df[b_col].astype(str).str.strip() == today_str]

# === 6. 提取 K列数据，截取前两个字并统计频率 ===
k_data = filtered_df[k_col].dropna().astype(str).str[:2]
freq = k_data.value_counts()

# === 7. 格式化输出 ===
output = ' '.join([f'{name}{count}' for name, count in freq.items()])

# === 8. 写入输出文件 ===
with open(output_txt, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"✅ 统计完成，输出结果如下：\n{output}")
print(f"📄 已写入：{output_txt}")
