from input_utils import get_search_and_filter, get_play_and_pages
from scraper import scrape
from save_utils import save_to_excel

def main():
    search_bar_keyword, filter_keywords_input = get_search_and_filter()
    if not search_bar_keyword or not filter_keywords_input:
        print("未输入关键词，程序退出。")
        return

    filter_keywords = [k.strip() for k in filter_keywords_input.split("+") if k.strip()]
    min_play_num, max_pages = get_play_and_pages()

    results = scrape(search_bar_keyword, filter_keywords, min_play_num, max_pages)
    save_to_excel(results, search_bar_keyword, filter_keywords_input, min_play_num)

if __name__ == "__main__":
    main()
