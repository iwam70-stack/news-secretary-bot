import requests
from bs4 import BeautifulSoup
import datetime

WATCH_LIST = ["震災", "暴風", "衝突", "大勝", "静岡", "藤枝"]

def run():
    url = "https://www.yahoo.co.jp/"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    all_links = soup.find_all('a', href=True)

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_text = f"\n=== ニュースレポート ({now_str}) ===\n"
    
    for item in all_links:
        link = item.get("href")
        title = item.text.strip()
        if 'news.yahoo.co.jp/pickup' in link and title:
            is_important = any(word in title for word in WATCH_LIST)
            mark = "★【特報】" if is_important else "・"
            report_text += f"{mark} {title}\n"
    
    # 結果をファイルに書き出す
    with open("daily_report.txt", "a", encoding="utf-8") as f:
        f.write(report_text)
    
    print("ファイルへの書き出しが完了しました。")

if __name__ == "__main__":
    run()
# 最新のニュースだけを「mail_body.txt」として保存
    with open("mail_body.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
