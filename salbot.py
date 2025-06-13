import streamlit as st
import openai
import os
import base64

st.set_page_config(page_title="SalBot - The Feisty Chatbot", layout="wide")

custom_css = """
<style>
    .main {
        background-color: #0e1117;
        color: #f5f5f5;
        font-family: 'Courier New', monospace;
    }
    .stTextInput input {
        background-color: #1c1e26;
        color: #f5f5f5;
    }
    .stChatMessage { 
        border-radius: 12px; 
        padding: 10px; 
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #1f77b4;
        color: white;
    }
    .stChatMessage.assistant {
        background-color: #e74c3c;
        color: white;
    }
    .block-container {
        padding-top: 2rem;
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
    openai.api_key = api_key

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
                    response = openai.ChatCompletion.create(
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