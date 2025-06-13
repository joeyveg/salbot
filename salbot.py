import streamlit as st
import openai
import os
import base64

st.set_page_config(page_title="SalBot - The Feisty Chatbot", layout="wide")

custom_css = """
<style>
    html, body, [class*="css"]  {
        background-color: #1a1a1a;
        color: #f4f4f4;
        font-family: 'Fira Code', monospace;
    }
    .stTextInput input {
        background-color: #2d2d2d;
        color: #fff;
        border: 1px solid #555;
        border-radius: 8px;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .stChatMessage.user {
        background: linear-gradient(to right, #444, #666);
        color: #fff;
    }
    .stChatMessage.assistant {
        background: linear-gradient(to right, #e74c3c, #c0392b);
        color: #fff;
    }
    .stButton>button {
        background-color: #c0392b;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
    }
    .stSelectbox div, .stTextInput label {
        color: #bbb;
    }
    h1 {
        color: #ff6b6b;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("🌶️ SalBot - Your Feisty Chat Companion")

st.markdown("""
Welcome to **SalBot** — the sassiest AI on the block. Powered by OpenAI, this chatbot doesn't hold back. 
Ask anything, but don’t expect sugar-coated answers. 🍸
""")

api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")
model = st.selectbox("🤖 Choose a model", ["gpt-4", "gpt-3.5-turbo"])

if api_key:
    client = openai.OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are SalBot. You are clever, sharp-tongued, and brutally honest, but still helpful and intelligent."}
        ]

    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Say something spicy to SalBot...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Mixing up some hot takes..."):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=st.session_state.messages,
                        temperature=0.95
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"Something went wrong. Probably your fault. Error: {str(e)}"

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
else:
    st.info("SalBot needs your API key to serve some truth.")