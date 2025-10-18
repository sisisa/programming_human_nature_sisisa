import streamlit as st
from janome.tokenizer import Tokenizer
import json

st.title("性格をプログラミング言語に変換するアプリ")

# 入力欄
name = st.text_input("名前を入力してください")
personality = st.text_area("性格（性質）を入力してください")

# 類似語辞書
similar_keywords = {
    "冷静": ["落ち着き", "クール", "慎重", "穏やか"],
    "論理的": ["理性的", "思考的", "分析的"],
    "自由": ["のびのび", "柔軟", "マイペース"],
    "親しみやすい": ["フレンドリー", "やさしい", "人懐っこい"],
    "真面目": ["誠実", "まっすぐ", "堅実"],
    "クリエイティブ": ["創造的", "発想", "アイデア"],
    "完璧主義": ["几帳面", "丁寧", "こだわり"]
}

# 分析ボタン
if st.button("変換する"):
    if not personality:
        st.warning("性格を入力してください。")
    else:
        # --- 形態素解析 ---
        t = Tokenizer()
        tokens = [token.surface for token in t.tokenize(personality)
                  if '形容詞' in token.part_of_speech or '名詞' in token.part_of_speech]

        # --- JSON読込 ---
        with open("languages.json", encoding="utf-8") as f:
            data = json.load(f)

        # --- スコア計算 ---
        scores = {lang: 0 for lang in data.keys()}

        for word in tokens:
            for lang, info in data.items():
                for keyword in info["keywords"]:
                    # 完全一致 or 部分一致
                    if keyword in word or word in keyword:
                        scores[lang] += 2
                    # 類似語の一致
                    if keyword in similar_keywords:
                        for syn in similar_keywords[keyword]:
                            if syn in word or word in syn:
                                scores[lang] += 1

        best_lang = max(scores, key=scores.get)
        desc = data[best_lang]["description"]

        # --- 結果表示 ---
        st.success(f"{name}さんは「{best_lang}タイプ」です！")
        st.write(desc)
        st.write("---")
        st.write("【抽出された単語】", tokens)
        st.write("【スコア】", scores)
