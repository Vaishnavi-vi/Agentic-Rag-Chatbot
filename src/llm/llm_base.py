from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint # Replace with your LLM
import os
from langsmith import traceable

@traceable(name="load_llm_model", tags=["llm", "huggingface"])
def get_llm(api_key: str = None):
    api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    llm_endpoint = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-20b",
        temperature=0.7,
        task="text_generation",
        model_kwargs={"api_key": api_key}
    )
    return ChatHuggingFace(llm=llm_endpoint)

model = get_llm(api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"))