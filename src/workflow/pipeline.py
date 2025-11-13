from src.llm.llm_with_tools import model_with_tool
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode
from src.state import Agentstate
from langgraph.checkpoint.memory import InMemorySaver


from src.nodes.chat_model import chat_model
from src.nodes.rag_node import rag_node
from src.nodes.generate_rag import generate_rag
from src.nodes.tool_node import tool_node
from src.nodes.generate_tool import generate_tool_response
import warnings
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=r".*google\.api_core.*"
)

def check_condition(state: Agentstate):
    latest_message = next(
        (m.content.lower() for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        ""
    )

    rag_keywords = [
        "explain", "describe", "define", "tell me about", 
        "information", "details on", "who is", "why does"
    ]
    tool_keywords = [
        "bmi", "body mass", "calculate", "compute", "math", "sum", "add", "subtract",
        "divide", "multiply", "square root", "convert", "exchange rate", "currency",
        "usd", "inr", "euro", "dollar", "stock", "share", "price", "market", "equity",
        "weather", "temperature", "forecast", "climate",
        "news", "ai update", "ai news", "latest ai", "tech news", "technology","when was","history of"
    ]

    if any(kw in latest_message for kw in rag_keywords):
        print("Routing to RAG")
        return "rag_node"
    elif any(kw in latest_message for kw in tool_keywords):
        print("Routing to TOOL")
        return "tool_node"
    else:
        print("Routing to CHAT")
        return "END"
    

graph=StateGraph(Agentstate)
checkpointer=InMemorySaver()

graph.add_node("chat_model",chat_model)
graph.add_node("rag_node",rag_node)
graph.add_node("tool_node",tool_node)
graph.add_node("generate_rag",generate_rag)
graph.add_node("generate_tool",generate_tool_response)

graph.add_edge(START,"chat_model")
graph.add_conditional_edges(
    "chat_model",
    check_condition,
    {"rag_node": "rag_node", "tool_node": "tool_node", "END": END}
)

graph.add_edge("rag_node", "generate_rag")
graph.add_edge("tool_node", "generate_tool")
graph.add_edge("generate_rag", END)
graph.add_edge("generate_tool", END)
graph.add_edge("chat_model", END)


workflow=graph.compile(checkpointer=checkpointer)
workflow
    

    

