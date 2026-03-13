import requests
from bs4 import BeautifulSoup
import datetime

def get_x_trends():
    url = "https://search.yahoo.co.jp/realtime"
    try:
        # User-Agentを設定して、ブラウザからのアクセスに見せかけます
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        
        # 2026年現在のYahoo!リアルタイム検索のトレンド項目を抽出
        # ランキングのテキストが入っている要素を特定します
        trends = []
        # aタグ内のテキストがトレンドワードになっています
        rank_items = soup.select('section > ol > li a') 
        
        for i, item in enumerate(rank_items[:10], 1):
            # 余計な空白や改行を削ってリスト化
            word = item.text.strip().replace('\n', '')
            trends.append(f"{i}位: {word}")
        
        return "\n".join(trends) if trends else "トレンドが見つかりませんでした。"
    except Exception as e:
        return f"トレンド取得エラー: {e}"

# --- 追加する解説関数 ---
def get_ai_explanation(word_list):
    try:
        # モデル名は必ず「本名」で！
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        prompt = f"以下のトレンドワードについて、それぞれ何が起きているか15文字以内で簡潔に解説してください。\n\n" + "\n".join(word_list)
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # ここが肝！エラーが出ても、システムは止めずに「空」を返す
        return f"（AI解説は現在お休み中です: {e}）"

def run():
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    trends = get_x_trends() # リスト形式で取得するように少し改造
    
    # トレンドがあればAIに解説を頼む（失敗しても死なない）
    ai_comment = get_ai_explanation(trends) if trends else "トレンドなし"
    
    report = f"【朝イチのXトレンド報告】\n作成日時: {now_str}\n\n{trends_text}"
    print(report) # ログ確認用
    
    # メール送信用ファイルに書き出し
    with open("mail_body.txt", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    run()
