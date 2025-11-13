from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.workflow.pipeline import workflow
from fastapi.responses import StreamingResponse

app = FastAPI(title="Agentic RAG Chatbot API")

class QueryRequest(BaseModel):
    query: str

@app.get("/about")
def root():
    return {"response":"Agentic Rag Chatbot with multi tool Integration"}

@app.get("/health")
def root():
    return {"status": "running"}

@app.post("/chat/stream")
def chat_stream(req: QueryRequest):
    """Stream token-by-token model output"""

    initial_state = {"messages": [HumanMessage(content=req.query)]}
    config = {"configurable": {"thread_id": "1"}}

    def generate():
        try:
            # Stream messages as they come from workflow
            for message_chunk, metadata in workflow.stream(
                initial_state, config, stream_mode="messages"
            ):
                if message_chunk.content:
                    # Send chunk as it arrives
                    yield message_chunk.content + " "
        except Exception as e:
            yield f"\nError: {e}"

    # Stream it as plain text to client
    return StreamingResponse(generate(), media_type="text/plain")

