from fastapi import FastAPI
from datetime import datetime
import json
import os
from pydantic import BaseModel
from typing import Optional, List

from langchain_ollama import OllamaLLM
import chromadb
from chromadb.config import Settings

from orchestration.graph import market_graph

# ---------------- APP SETUP ----------------

app = FastAPI(
    title="Market Intelligence AI",
    description="Multi-agent market research system using LangGraph + Ollama + RAG",
    version="2.0"
)

OUTPUT_DIR = "outputs"
VECTOR_DIR = "vector_store"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

# ---------------- VECTOR DB (FIXED STEP 2) ----------------
# ❌ NO LangChain embeddings here
# ✅ Pure ChromaDB native client

chroma_client = chromadb.Client(
    Settings(
        persist_directory=VECTOR_DIR,
        anonymized_telemetry=False
    )
)

collection = chroma_client.get_or_create_collection(
    name="market_reports"
)

# ---------------- MODELS ----------------

class AnalyzeRequest(BaseModel):
    industry: str
    from_date: str
    to_date: str
    focus: Optional[str] = None

class ChatRequest(BaseModel):
    report_id: str
    question: str

# ---------------- UTILS ----------------

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# ---------------- ANALYZE ----------------

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    """
    Runs LangGraph, saves report, chunks it, and stores embeddings.
    """

    # 1️⃣ Build topic
    topic = (
        f"{request.industry} market analysis "
        f"from {request.from_date} to {request.to_date}"
    )
    if request.focus:
        topic += f" with focus on {request.focus}"

    # 2️⃣ Run LangGraph
    result = market_graph.invoke({"topic": topic})
    final_report = result["final"]

    # 3️⃣ Save report file
    report_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{request.industry.lower().replace(' ', '_')}_{report_id}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)

    # 4️⃣ Chunk report
    report_text = json.dumps(final_report, ensure_ascii=False)
    chunks = chunk_text(report_text)

    # 5️⃣ Store chunks in ChromaDB (auto-embedding)
    collection.add(
        documents=chunks,
        metadatas=[{"report_id": report_id}] * len(chunks),
        ids=[f"{report_id}_{i}" for i in range(len(chunks))]
    )

    return {
        "message": "Analysis completed",
        "report_id": report_id,
        "saved_file": filepath,
        "chunks_stored": len(chunks)
    }

# ---------------- CHAT (FULL RAG) ----------------

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Answers questions using vector search + report context.
    """

    # 1️⃣ Retrieve relevant chunks
    results = collection.query(
        query_texts=[request.question],
        n_results=4,
        where={"report_id": request.report_id}
    )

    retrieved_chunks = results["documents"][0]

    if not retrieved_chunks:
        return {"error": "No relevant data found for this report"}

    # 2️⃣ Build RAG prompt
    context = "\n\n".join(retrieved_chunks)

    llm = OllamaLLM(model="llama3")

    prompt = f"""
You are a market intelligence analyst.

Answer the question ONLY using the context below.
If the answer is not present, say "Not found in report".

CONTEXT:
{context}

QUESTION:
{request.question}
"""

    answer = llm.invoke(prompt)

    # 3️⃣ Save chat output
    chat_file = f"chat_{request.report_id}_{datetime.now().strftime('%H%M%S')}.json"
    chat_path = os.path.join(OUTPUT_DIR, chat_file)

    with open(chat_path, "w", encoding="utf-8") as f:
        json.dump({
            "report_id": request.report_id,
            "question": request.question,
            "answer": answer,
            "chunks_used": retrieved_chunks
        }, f, indent=2, ensure_ascii=False)

    return {
        "answer": answer,
        "saved_chat": chat_path
    }

# ---------------- HEALTH ----------------

@app.get("/health")
def health():
    try:
        llm = OllamaLLM(model="llama3")
        llm.invoke("ping")
        return {"status": "ok", "ollama": "running"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.get("/")
def health_check():
    return {"status": "Market Intelligence AI is running"}
