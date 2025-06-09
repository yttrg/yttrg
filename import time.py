import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from parse_utils import parse_play_count

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

def scrape(search_bar_keyword, filter_keywords, min_play_num, max_pages):
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
    return results
