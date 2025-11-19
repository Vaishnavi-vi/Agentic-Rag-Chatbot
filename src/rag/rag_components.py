from langsmith import traceable
from googleapiclient.discovery import build
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()


@traceable(name="google_search", tags=["rag", "search"])
def google_search(query: str, limit: int, api_key: str, cse_id: str):
    service = build("customsearch", "v1", developerKey=api_key)
    response = service.cse().list(q=query, cx=cse_id, num=limit).execute()
    urls = [item.get("link") for item in response.get("items", [])][:limit]
    return urls


@traceable(name="load_web_docs", tags=["rag", "loader"])
def load_web_docs(urls: list[str]):
    docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        docs.extend(loader.load())
    return docs


@traceable(name="split_documents", tags=["rag", "splitter"])
def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)


@traceable(name="embed_and_store", tags=["rag", "vectorstore"])
def embed_and_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="my_data"
    )


@traceable(name="retrieve_docs", tags=["rag", "retriever"])
def retrieve_docs(vectorstore, query: str, k: int = 3):
    retriever = vectorstore.as_retriever(
        search_kwargs={"k":k},
        search_type="similarity"
    )
    return retriever.invoke(query)


@traceable(name="format_docs", tags=["rag"])
def format_docs(docs):
    seen = set()
    unique_contents = []

    for d in docs:
        text = d.page_content.strip()
        if text not in seen:
            unique_contents.append(text)
            seen.add(text)

    return "\n\n".join(unique_contents)

