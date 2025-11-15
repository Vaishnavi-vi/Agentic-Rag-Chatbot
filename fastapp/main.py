from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.workflow.pipeline import workflow
from fastapi.responses import StreamingResponse

app = FastAPI(title="Agentic RAG Chatbot API")

class QueryRequest(BaseModel):
    query: str

@app.get("/about")
def about():
    return {"response": "Agentic Rag Chatbot with multi tool Integration"}

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/chat/stream")
def chat_stream(req: QueryRequest):

    initial_state = {"messages": [HumanMessage(content=req.query)]}
    config = {"configurable": {"thread_id": "1"}}

    def generate():
        try:
            for message_chunk, metadata in workflow.stream(
                initial_state, config, stream_mode="messages"
            ):
                # Case 1: LangChain message (AIMessage etc.)
                if hasattr(message_chunk, "content"):
                    if message_chunk.content:
                        yield message_chunk.content

                # Case 2: plain string
                else:
                    yield str(message_chunk)

        except Exception as e:
            yield f"\nError: {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")





