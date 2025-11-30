import streamlit as st
import requests
import uuid
from PIL import Image

# ------------------- CONFIG ------------------- 
FASTAPI_STREAM_URL = "http://127.0.0.1:8000/chat/stream"
FASTAPI_HISTORY_URL = "http://127.0.0.1:8000/chat/history"

# ------------------- UTILITY FUNCTIONS ------------------- 

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_thread"]:
        st.session_state["chat_thread"].append(thread_id)

def load_conversation(thread_id):
    """Load message history from FastAPI"""
    try:
        resp = requests.get(f"{FASTAPI_HISTORY_URL}/{thread_id}")
        data = resp.json()
        return data.get("messages", [])
    except:
        return []


# ------------------- SESSION SETUP ------------------- 

st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="💬", layout="centered")

page = st.sidebar.radio("Go to", ["Home", "Agentic Rag Chatbot"])

if page == "Home":
    st.header(" 💬 Agentic RAG Chatbot")
    image = Image.open("C:\\Users\\Dell\\Downloads\\Rag chatbot.png")
    st.image(image, use_container_width=True)

elif page == "Agentic Rag Chatbot":
    st.title("💬 Agentic RAG Chatbot with Multi Tool Integration")
    st.write("Ask anything — I’ll use tools, RAG, or knowledge to answer!")

    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generate_thread_id()

    if "chat_thread" not in st.session_state:
        st.session_state["chat_thread"] = []

    add_thread(st.session_state["thread_id"])


# ------------------- SIDEBAR ------------------- 

    st.sidebar.title("Chatbot Controls")

    if st.sidebar.button("New Chat"):
        reset_chat()

    st.sidebar.header("My Conversations")
    for tid in st.session_state["chat_thread"]:
        if st.sidebar.button(tid):
            st.session_state["thread_id"] = tid
            msgs = load_conversation(tid)

            formatted = []
            for m in msgs:
                role = "user" if m["type"] == "HumanMessage" else "assistant"
                formatted.append({"role": role, "content": m["content"]})

            st.session_state["message_history"] = formatted


# ------------------- DISPLAY CHAT HISTORY ------------------- #

    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# - User Input Handling ------------------- #

    user_input = st.chat_input("Type here...")

    if user_input:
        st.session_state["message_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        payload = {
        "thread_id": st.session_state["thread_id"],
        "query": user_input
        }

        with st.chat_message("assistant"):
            placeholder = st.empty()
            collected_text = ""

            try:
                response = requests.post(
                FASTAPI_STREAM_URL,
                json=payload,
                stream=True)

                for chunk in response.iter_content(chunk_size=None):
                    decoded = chunk.decode("utf-8")
                    collected_text += decoded
                    placeholder.write(collected_text)

            except Exception as e:
                collected_text = f"Error: {str(e)}"
                placeholder.write(collected_text)


        st.session_state["message_history"].append(
            {"role": "assistant", "content": collected_text})
    




