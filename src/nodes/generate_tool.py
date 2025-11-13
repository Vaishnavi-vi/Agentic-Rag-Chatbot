from src.state import Agentstate
from langchain_core.messages import AIMessage,ToolMessage,HumanMessage
from src.llm.llm_with_tools import model_with_tool


from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser

def generate_tool_response(state: Agentstate):
    """Use LLM to turn structured tool output into a clean, readable summary."""
    tool_messages = [m for m in state["messages"] if isinstance(m, ToolMessage)]
    if not tool_messages:
        return {"messages": [AIMessage(content="No tool output found.")]}

    latest_tool_output = tool_messages[-1].content

    # Define your summarization prompt
    prompt = PromptTemplate(
        input_variables=["tool_output"],
        template=(
            "You are a helpful AI assistant. A tool has just returned this structured result:\n"
            "```{tool_output}```\n\n"
            "Your task:\n"
            "- Interpret this result accurately.\n"
            "- Explain it in plain, human-readable English.\n"
            "- Do **not** show JSON, code, or key-value pairs.\n"
            "- Respond conversationally as if talking to the user.\n"
            "- Keep it short (2–3 sentences max).\n\n"
            "Now write your response:"
        ),
    )

    # Combine prompt + model + parser in a simple chain
    parser = StrOutputParser()
    chain = prompt | model_with_tool | parser

    response = chain.invoke({"tool_output": latest_tool_output})
    return {"messages": [response]}
