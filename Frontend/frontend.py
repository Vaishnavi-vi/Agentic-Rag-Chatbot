import streamlit as st
import requests

# FastAPI streaming endpoint
FASTAPI_URL = "http://127.0.0.1:8000/chat/stream"

st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="💬", layout="centered")

st.title("💬 Agentic RAG Chatbot")
st.write("Ask anything — I’ll use tools, RAG, or knowledge to answer!")

# Initialize chat history
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# Display previous messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your question here...")

def get_streamed_response(query):
    """Read streaming response from FastAPI"""
    try:
        with requests.post(FASTAPI_URL, json={"query": query}, stream=True) as r:
            if r.status_code != 200:
                yield f"Server error: {r.status_code}"
            else:
                for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        yield chunk
    except requests.exceptions.RequestException as e:
        yield f"Connection error: {e}"

# Handle user input
if user_input:
    # Display user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant response as it streams
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        streamed_text = ""

        for chunk in get_streamed_response(user_input):
            streamed_text += chunk
            message_placeholder.markdown(streamed_text)

        st.session_state["message_history"].append({"role": "assistant", "content": streamed_text})

