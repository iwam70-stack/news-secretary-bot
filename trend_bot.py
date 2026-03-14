import requests
from bs4 import BeautifulSoup
import datetime

def get_x_trends():
    url = "https://search.yahoo.co.jp/realtime"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        
        trends_list = []
        # トレンドの各項目（li要素）を取得
        items = soup.select('section > ol > li')
        
        for i, item in enumerate(items[:10], 1):
            word_element = item.select_one('a')
            if word_element:
                word = word_element.text.strip()
                # 🔗 リンク（href）を取得して、絶対URLに変換
                link = word_element.get('href')
                if link and link.startswith('/'):
                    link = "https://search.yahoo.co.jp" + link
            else:
                word, link = "不明", ""

            # レポートの作成（ワード、リンク、説明の3点セット）
            trends_list.append(f"{i}位: {word}\n   🔗 {link}\n   👉 詳細は上記URLでチェック！")
            
        return "\n\n".join(trends_list) if trends_list else "トレンドが見つかりませんでした。"
    except Exception as e:
        return f"トレンド取得エラー: {e}"

def run():
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content = get_x_trends()
    
    report = f"【朝イチのXトレンド報告（硬派版）】\n作成日時: {now_str}\n\n{content}"
    
    print(report) # ログ確認用
    
    # メール送信用ファイルに書き出し
    with open("mail_body.txt", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    run()
