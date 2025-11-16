from src.state import Agentstate
from src.llm.llm_with_tools import model_with_tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from langsmith import traceable


@traceable(name="generate_rag_final_answer", tags=["rag", "final_answer"])
def generate_rag(state: Agentstate):
    query = state["messages"][-1].content
    context = state.get("context", "")

    @traceable(name="generate_prompt")
    def build_prompt():
        return PromptTemplate(
            template=(
                "You are a powerful assistant.\n"
                "Generate a short and correct final answer using ONLY this context:\n\n"
                "{context}\n\n"
                "User Question: {question}"
            ),
            input_variables=["context", "question"],
        )

    prompt = build_prompt()


    model = model_with_tool
    parser = StrOutputParser()

 
    @traceable(name="rag_llm_chain")
    def run_chain(context, query):
        chain = prompt | model | parser
        return chain.invoke({"context": context, "question": query})

    final_answer = run_chain(context, query)


    return {"messages": [AIMessage(content=final_answer)]}
