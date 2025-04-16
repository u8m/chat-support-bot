import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import pandas as pd
import io

# APIキー読み込み
load_dotenv("gpt-key.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# フォント設定
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Noto Sans JP', sans-serif;
        font-weight: 300;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# UI
st.title("💬 Chat GPT 問い合わせボット")
st.markdown("問い合わせ内容を入力してください👇")

# デザイン
st.markdown(
    """
<style>
    html, body, [class*="css"] {
        background-color: #111111;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stApp {
        background-color: #111111;
        color: #ffffff;
    }

    /* 質問・回答 吹き出し風デザイン */
    .chat-bubble-q {
        background-color: #222222;
        color: #ffffff;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .chat-bubble-a {
        background-color: #333333;
        color: #ffffff;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* ダウンロードボタンの色調整 */
    .stDownloadButton > button {
        background-color: #ffffff;
        color: #111111;
        border-radius: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# セッション状態で履歴を保持
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ユーザーからの入力
user_input = st.text_input("あなたの質問は？", "")

# 回答表示エリア
if user_input:
    with st.spinner("AIが考え中です..."):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは日本語で自然な敬語を使うAIアシスタントです。誤字や変な言い回しを避けて、正しい日本語で返答してください。",
                },
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
        )
        ai_reply = response.choices[0].message.content

        # 履歴に追加
        st.session_state.chat_history.append(
            {"question": user_input, "answer": ai_reply}
        )

# 履歴表示
if st.session_state.chat_history:
    st.markdown("### 🗂 過去の履歴")
    for idx, entry in enumerate(reversed(st.session_state.chat_history), start=1):
        st.markdown(
            f"<div class='chat-bubble-q'><strong>📝 質問 {idx}：</strong><br>{entry['question']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='chat-bubble-a'><strong>🤖 回答 {idx}：</strong><br>{entry['answer']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

# 履歴があるときだけダウンロードボタンを表示
if st.session_state.chat_history:
    df = pd.DataFrame(st.session_state.chat_history)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="📥 履歴をCSVでダウンロード",
        data=csv_data,
        file_name="chat_history.csv",
        mime="text/csv",
    )
