import streamlit as st

# タイトル
st.title("人の性質を入力するアプリ")

# 名前入力欄
name = st.text_input("名前を入力してください")
user_input = st.text_input("パスワードを入力してください",type="password")

# 性格入力欄（複数行テキスト）
personality = st.text_area("性格（性質）を入力してください")

# 送信ボタン
if st.button("送信"):
    st.write("### 入力結果")
    
    st.write(f"test: {user_input}")
    st.write(f"名前: {name}")
    st.write(f"性格: {personality}")
