import requests
from bs4 import BeautifulSoup

WATCH_LIST = ["震災", "暴風", "衝突", "大勝", "静岡", "藤枝"]

def run():
    url = "https://www.yahoo.co.jp/"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    all_links = soup.find_all('a', href=True)

    print("=== ニュースレポート ===")
    for item in all_links:
        link = item.get("href")
        title = item.text.strip()
        if 'news.yahoo.co.jp/pickup' in link and title:
            is_important = any(word in title for word in WATCH_LIST)
            mark = "★【特報】" if is_important else "・"
            print(f"{mark} {title}")

if __name__ == "__main__":
    run()
