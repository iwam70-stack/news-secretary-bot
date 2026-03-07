import requests
from bs4 import BeautifulSoup
import datetime
import os
import google.generativeai as genai

WATCH_LIST = ["震災", "暴風", "衝突", "大勝", "静岡", "藤枝"]

# Geminiの初期設定
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini通信エラー: {e}"

def run():
    url = "https://www.yahoo.co.jp/"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    all_links = soup.find_all('a', href=True)

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
                important_news_list.append(title)
    
    # --- ここからGeminiの出番 ---
    if important_news_list:
        news_str = "\n".join(important_news_list)
        prompt = f"以下のニュースを、地元の話題に興味がある人に向けて短く要約して、一言コメントを添えてください。\n\n{news_str}"
    else:
        prompt = "今日は注目キーワードに一致するニュースがありませんでした。仕事やプログラミングを頑張っている私に、短く励ましのメッセージを1つください。"
    
    ai_comment = ask_gemini(prompt)
    
    # メール用の本文作成
    with open("mail_body.txt", "w", encoding="utf-8") as f:
        f.write(f"【AI秘書からの報告】\n\n{ai_comment}")
    
    # 履歴保存
    with open("daily_report.txt", "a", encoding="utf-8") as f:
        f.write(report_text + f"\nAIコメント: {ai_comment}\n")

if __name__ == "__main__":
    run()
