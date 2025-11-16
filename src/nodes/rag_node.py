from langsmith import traceable
from src.rag.rag_components import google_search,load_web_docs,split_docs,embed_and_store,retrieve_docs,format_docs
import os
from src.state import Agentstate


@traceable(name="rag_node", tags=["rag", "node"])
def rag_node(state: Agentstate):

    query = state["messages"][-1].content.strip()

    google_api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")

    if not google_api_key or not cse_id:
        raise RuntimeError("Google API Key or CSE ID not set.")

    urls = google_search(query, limit=3,api_key=google_api_key,cse_id=cse_id)

    if not urls:
        return {"context": "No results found.", "messages": state["messages"]}

    docs = load_web_docs(urls)

    chunks = split_docs(docs)

    vectorstore = embed_and_store(chunks)

    retrieved_docs = retrieve_docs(vectorstore, query, k=3)

    context = format_docs(retrieved_docs)

    return {
        "context": context,
        "messages": state["messages"]
    }
