from src.state import Agentstate
from langchain_core.messages import AIMessage,ToolMessage,HumanMessage
from src.llm.llm_with_tools import model_with_tool
from langsmith import traceable
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser

@traceable(run_type="chain", name="generate_tool_response") 
def generate_tool_response(state: Agentstate):
    """Use LLM to turn structured tool output into a clean, readable summary."""
    tool_messages = [m for m in state["messages"] if isinstance(m, ToolMessage)]
    if not tool_messages:
        return {"messages": [AIMessage(content="No tool output found.")]}

    latest_tool_output = tool_messages[-1].content

    prompt = PromptTemplate(
    input_variables=["tool_output"],
    template=(
        "You are a helpful AI assistant. A tool returned the following data:\n"
        "{tool_output}\n\n"
        "Convert this into a clean, simple human-readable answer.\n"
        "\n"
        "STRICT RULES:\n"
        "• Do NOT show metadata.\n"
        "• Do NOT show JSON or key–value pairs.\n"
        "• Do NOT repeat the raw data.\n"
        "• Explain the result in natural, conversational English.\n"
        "• Keep it short **summary** (2–3 sentences).\n"
        "\n"
        "Human-friendly answer:"
    ),
)

    # Combine prompt + model + parser in a simple chain
    parser = StrOutputParser()
    chain = prompt | model_with_tool | parser

    response = chain.invoke({"tool_output": latest_tool_output})
    state["messages"].append(AIMessage(content=response.strip()))

    return {"messages": state["messages"]}
    # return {"messages": [AIMessage(content=response)],"replace_messages":True}
