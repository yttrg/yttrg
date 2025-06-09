import re

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
