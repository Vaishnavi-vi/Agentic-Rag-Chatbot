from src.state import Agentstate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.llm.llm_with_tools import model_with_tool
from langchain_core.messages import AIMessage



def generate_rag(state:Agentstate):
    query=state["messages"][-1].content
    context=state["context"]
    prompt=PromptTemplate(template=""" You are a Powerful assistant, Generate the final and short answer from the context {context} and provided question:{question} """,input_variables=["context","question"])
    model=model_with_tool
    parser=StrOutputParser()
    
    chain=prompt|model|parser
    
    response=chain.invoke({"context":context,"question":query})
    
    return {"messages":[AIMessage(content=response)]}