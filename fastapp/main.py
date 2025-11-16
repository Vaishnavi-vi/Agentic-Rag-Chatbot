# from fastapi import FastAPI
# from pydantic import BaseModel
# from langchain_core.messages import HumanMessage
# from src.workflow.pipeline import workflow
# from fastapi.responses import StreamingResponse

# app = FastAPI(title="Agentic RAG Chatbot API")

# class QueryRequest(BaseModel):
#     query: str

# @app.get("/about")
# def about():
#     return {"response": "Agentic Rag Chatbot with multi tool Integration"}

# @app.get("/health")
# def health():
#     return {"status": "running"}

# @app.post("/chat/stream")
# def chat_stream(req: QueryRequest):

#     initial_state = {"messages": [HumanMessage(content=req.query)]}
#     config = {"configurable": {"thread_id": "1"}}

#     def generate():
#         try:
#             for message_chunk, metadata in workflow.stream(
#                 initial_state, config, stream_mode="messages"
#             ):
#                 # Case 1: LangChain message (AIMessage etc.)
#                 if hasattr(message_chunk, "content"):
#                     if message_chunk.content:
#                         yield message_chunk.content

#                 # Case 2: plain string
#                 else:
#                     yield str(message_chunk)

#         except Exception as e:
#             yield f"\nError: {str(e)}"

#     return StreamingResponse(generate(), media_type="text/plain")


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from src.workflow.pipeline import workflow

app = FastAPI(title="Agentic RAG Chatbot API")

# ---- Request Models ---- #
class QueryRequest(BaseModel):
    thread_id: str
    query: str


# ---------------- About / Health ---------------- #
@app.get("/about")
def about():
    return {"response": "Agentic RAG Chatbot with Multi-Tool Integration"}

@app.get("/health")
def health():
    return {"status": "running"}


# ---------------- Resume Chat Endpoint ---------------- #
@app.get("/chat/history/{thread_id}")
def get_history(thread_id: str):
    """
    Return ALL messages stored in the LangGraph checkpointer.
    This allows frontend to resume old chats.
    """

    try:
        saved_state = workflow.get_state({"configurable": {"thread_id": thread_id}})
    except Exception:
        return {"messages": []}

    if not saved_state or "messages" not in saved_state.values:
        return {"messages": []}

    msgs = []
    for m in saved_state.values["messages"]:
        msgs.append({
            "type": m.__class__.__name__,
            "content": m.content
        })

    return {"messages": msgs}


# ---------------- Streaming Chat Endpoint ---------------- #
@app.post("/chat/stream")
def chat_stream(req: QueryRequest):

    initial_state = {"messages": [HumanMessage(content=req.query)]}

    config = {"configurable": {"thread_id": req.thread_id}}

    def generate():
        try:
            for msg, meta in workflow.stream(
                initial_state,
                config=config,
                stream_mode="messages"
            ):
                if hasattr(msg, "content") and msg.content:
                    yield msg.content
        except Exception as e:
            yield f"[ERROR]: {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")








