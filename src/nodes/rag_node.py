from src.state import Agentstate
import os
from googleapiclient.discovery import build
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings



def rag_node(state: Agentstate):
    query=state["messages"][-1].content.strip()
    limit=3
    google_api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID") 
    if not google_api_key or not cse_id:
        raise RuntimeError("Please set Google APi Key in your environment.")
    
    try:
        service = build("customsearch", "v1", developerKey=google_api_key)
        response = service.cse().list(q=query,cx=cse_id,num=limit).execute()
        urls = [item.get("link") for item in response.get("items", [])][:limit]
    except Exception as e:
        print("Error retrieving URLs:", e)
        urls = []

    if not urls:
        return {"context": "No relevant information found.", "messages": state["messages"]}

    
    #Document loader  
    docs=[]
    for url in urls:
        loader=WebBaseLoader(url)
        docs.extend(loader.load())
        
    #Text-splitter
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200)
    
    chunks=text_splitter.split_documents(docs)
    
    #embedding
    embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    #vector_store
    vector_store=Chroma.from_documents(
        embedding=embedding,
        documents=chunks,
        collection_name="my_data"
    )
    retriver=vector_store.as_retriever(search_kwargs={"k":3},search_type="similarity")
    retrieved_docs=retriver.invoke(query)
    
    def format_docs(docs):
        return "\n".join(doc.page_content for doc in docs)
    
    context=format_docs(retrieved_docs)
    
    return {"context":context}