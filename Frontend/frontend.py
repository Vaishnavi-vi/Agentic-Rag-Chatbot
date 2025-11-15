import streamlit as st
import requests
from PIL import Image
import uuid

FASTAPI_STREAM_URL = "http://127.0.0.1:8000/chat/stream"

st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="💬", layout="centered")

page = st.sidebar.radio("Go to", ["Home", "Agentic Rag Chatbot"])

if page == "Home":
    st.header(" 💬 Agentic RAG Chatbot")
    image = Image.open("C:\\Users\\Dell\\Downloads\\Rag chatbot.png")
    st.image(image, use_container_width=True)

elif page == "Agentic Rag Chatbot":
    st.title("💬 Agentic RAG Chatbot")
    st.write("Ask anything — I’ll use tools, RAG, or knowledge to answer!")

    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    st.sidebar.title("Chatbot Controls")

    if st.sidebar.button("New Chat"):
        st.session_state["message_history"] = []

    st.sidebar.header("My Conversations")

    # Display previous chat history
    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your question here...")

    def get_streamed_response(query):
        try:
            with requests.post(FASTAPI_STREAM_URL, json={"query": query}, stream=True) as r:
                if r.status_code != 200:
                    yield f"Server error: {r.status_code}"
                else:
                    for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            yield chunk
        except requests.exceptions.RequestException as e:
            yield f"Connection error: {e}"

    if user_input:
        st.session_state["message_history"].append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            streamed_text = ""

            for chunk in get_streamed_response(user_input):
                streamed_text += chunk
                message_placeholder.markdown(streamed_text)

        st.session_state["message_history"].append({"role": "assistant", "content": streamed_text})




