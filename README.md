# Agentic RAG Chatbot with Multi-Tool Integration

An **Agentic Retrieval-Augmented Generation (RAG) Chatbot** powered by an intelligent agent that can **dynamically choose and orchestrate multiple tools** (retrieval, web search, calculator, code execution, APIs, etc.) to answer complex user queries accurately and efficiently.

This project demonstrates **agentic reasoning + multi-tool execution + RAG**, making it highly relevant for real-world AI/ML and LLM system design.

---

## ✨ Key Features

* **Agentic Decision-Making**: The agent reasons step-by-step and decides *which tool(s)* to invoke
* **Multi-Tool Integration**:

  * Vector Retriever (RAG)
  * Web Search Tool
  * Calculator / Math Tool
  * Code / Python Tool
  * Custom API Tools (extensible)
* **RAG Pipeline**: Retrieves relevant document chunks before generation
* **Tool Chaining**: Agent can call **multiple tools in sequence** for a single query
* **Conversation Memory**: Maintains context across turns
* **Hallucination Reduction**: Answers are grounded in retrieved or tool-generated data
* **Modular & Scalable Design**

---

## 🧠 System Architecture

```
User Query
   ↓
Agent (Planner + Reasoner)
   ↓ decides
┌──────────────────────────────┐
│ Available Tools              │
│  • Vector Retriever (RAG)    │
│  • Web Search                │
│  • Calculator                │
│  • Python / Code Executor    │
│  • Custom APIs               │
└──────────────────────────────┘
   ↓
Tool Outputs / Retrieved Context
   ↓
LLM Generator
   ↓
Final Grounded Answer
```

---

## 🛠 Tech Stack

* **Language**: Python 3.10+
* **LLM**: OpenAI / Azure OpenAI / Local LLM
* **Agent Framework**: LangChain Agents / LlamaIndex Agents
* **Embeddings**: OpenAI / Sentence-Transformers
* **Vector Store**: FAISS / Chroma / Pinecone
* **Backend**: FastAPI
* **Frontend (Optional)**: Streamlit / React

---

## 🧰 Integrated Tools

| Tool             | Purpose                                      |
| ---------------- | -------------------------------------------- |
| Vector Retriever | Document-based question answering (RAG)      |
| Web Search Tool  | Real-time / external knowledge               |
| Calculator Tool  | Numerical & logical computations             |
| Python Tool      | Data processing, validation, transformations |
| Custom API Tool  | Domain-specific integrations                 |

The agent **autonomously selects** the appropriate tool(s) based on the query.

---

## ⚙️ Setup & Installation

1. Clone the repository
2. Create & activate a virtual environment
3. Install dependencies
4. Configure environment variables

---
## 🚀 Running the Application

### Start API Server

```bash
uvicorn fastapp.main:app --reload
```

### Optional UI

```bash
streamlit run frontend/frontend.py
```

---

## 🔮 Future Enhancements
* Feedback-based agent learning
* Docker & cloud deployment

---

## 📜 License

MIT License

---

## 👩‍💻 Author

**Vaishnavi Barolia**
AI / ML Research Intern Evostra Ventures

---

This project highlights **agentic reasoning + multi-tool orchestration**, aligning strongly with modern **LLM Engineer / AI Engineer** roles.
