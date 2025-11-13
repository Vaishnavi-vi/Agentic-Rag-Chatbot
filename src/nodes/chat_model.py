from src.llm.llm_with_tools import model_with_tool
from langchain_core.messages import AIMessage
from src.state import Agentstate


def chat_model(state: Agentstate):
    messages = state["messages"]
    response = model_with_tool.invoke(messages)
    return {"messages": messages + [response]}

