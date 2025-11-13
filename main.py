# main.py
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# ---- Load Environment Variables ----
load_dotenv()

# ---- Import your compiled workflow ----
from src.workflow.pipeline import workflow

# ---- Run the Chatbot ----
if __name__ == "__main__":
    thread_id = "1"
    query = input("Enter your query: ")  # e.g. "What is weather in Delhi?"
    
    # Initial state
    initial_state = {"messages": [HumanMessage(content=query)]}
    config = {"configurable": {"thread_id": thread_id}}

    try:
        for message_chunk,metadata in workflow.stream(initial_state,config,stream_mode="messages"):
            if message_chunk.content:
                print(message_chunk.content,end="",flush=True)
    except Exception as e:
        print(f"\n Error: {e}")

