import requests
from bs4 import BeautifulSoup
import datetime
import os

WATCH_LIST = ["震災", "暴風", "衝突", "大勝", "静岡", "藤枝"]

def run():
    url = "https://www.yahoo.co.jp/"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    all_links = soup.find_all('a', href=True)

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # ここで report_text を定義し始めます
    report_text = f"\n=== ニュースレポート ({now_str}) ===\n"
    
    important_news_list = []
    
    for item in all_links:
        link = item.get("href")
        title = item.text.strip()
        if 'news.yahoo.co.jp/pickup' in link and title:
            is_important = any(word in title for word in WATCH_LIST)
            mark = "★【特報】" if is_important else "・"
            report_text += f"{mark} {title}\n"
            if is_important:
                important_news_list.append(f"{mark} {title}")
    
    # 全件を daily_report.txt に追記（履歴用）
    with open("daily_report.txt", "a", encoding="utf-8") as f:
        f.write(report_text)
    
    # 最新の「重要ニュースだけ」を mail_body.txt に書き出す（メール用）
    # 重要ニュースがない場合はその旨を記載
    with open("mail_body.txt", "w", encoding="utf-8") as f:
        if important_news_list:
            f.write("\n".join(important_news_list))
        else:
            f.write("本日は指定したキーワードに一致する重要ニュースはありませんでした。")
    
    print("ファイルへの書き出しが完了しました。")

if __name__ == "__main__":
    run()
