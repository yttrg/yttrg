import pandas as pd
from datetime import datetime, timedelta

# === 1. 路径配置 ===
excel_path = r"C:\Users\UserComputer\Desktop\崔震林投放表.xlsx"
map_path = r"C:\Users\UserComputer\Desktop\账号映射表.xlsx"
output_txt = r"C:\Users\UserComputer\Desktop\代投统计.txt"

# === 2. 读取数据表和账号映射表 ===
xls = pd.ExcelFile(excel_path)
df_data = xls.parse(sheet_name=1)  # 第二个工作表：视频投放
df_map = pd.read_excel(map_path)  # 映射表：账号名称 - 账号来源

# === 3. 清洗列名 ===
df_data.columns = df_data.columns.map(str).str.strip()
df_map.columns = df_map.columns.map(str).str.strip()

# === 4. 获取列名 ===
date_col = df_data.columns[1]     # 第二列：日期（如 6.9）
account_col = df_data.columns[5]  # 第六列：账号名称

# === 5. 将字符串日期转为标准日期对象 ===
def str_to_date(s):
    try:
        return datetime.strptime(f"{datetime.now().year}.{s.strip()}", "%Y.%m.%d").date()
    except:
        return None

df_data[date_col] = df_data[date_col].astype(str)
df_data["日期_obj"] = df_data[date_col].apply(str_to_date)

# === 6. 计算时间区间（上周二 ~ 本周一）===
def get_last_weekday(base_date, weekday):
    return base_date - timedelta(days=(base_date.weekday() - weekday) % 7)

today = datetime.now()
this_monday = get_last_weekday(today, 0)
last_tuesday = get_last_weekday(this_monday - timedelta(days=1), 1)

# 7. 筛选符合日期的数据
df_filtered = df_data[
    (df_data["日期_obj"] >= last_tuesday.date()) &
    (df_data["日期_obj"] <= this_monday.date())
]

# === 8. 映射账号来源 ===
map_dict = dict(zip(df_map["账号名称"], df_map["账号来源"]))
df_filtered["账号来源"] = df_filtered[account_col].map(map_dict)

# === 9. 统计每个账号来源的数量 ===
result = df_filtered["账号来源"].value_counts().dropna()

# === 10. 输出到文本 ===
output_lines = [f"{name} {count}" for name, count in result.items()]
output_text = '\n'.join(output_lines)

with open(output_txt, 'w', encoding='utf-8') as f:
    f.write(output_text)

# === 11. 打印输出 ===
print(f"✅ 统计完成，时间范围：{last_tuesday} 至 {this_monday}")
print(f"📄 输出文件：{output_txt}")
print(output_text)
