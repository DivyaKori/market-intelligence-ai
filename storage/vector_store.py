import chromadb
from chromadb.config import Settings
from langchain_ollama import OllamaEmbeddings

# -------------------------------
# Embedding Model (Local, Open-Source)
# -------------------------------
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"   # Best for RAG with Ollama
)

# -------------------------------
# ChromaDB Client (Persistent)
# -------------------------------
client = chromadb.Client(
    Settings(
        persist_directory="vector_db",
        anonymized_telemetry=False
    )
)

# -------------------------------
# Vector Collection
# -------------------------------
collection = client.get_or_create_collection(
    name="market_reports",
    embedding_function=embeddings
)

# -------------------------------
# Store Report Chunks
# -------------------------------
def store_chunks(chunks, report_id):
    """
    Stores text chunks as vectors in ChromaDB
    """
    collection.add(
        documents=chunks,
        metadatas=[{"report_id": report_id}] * len(chunks),
        ids=[f"{report_id}_{i}" for i in range(len(chunks))]
    )

# -------------------------------
# Search Relevant Chunks
# -------------------------------
def search_chunks(query, report_id, k=5):
    """
    Performs semantic search over stored report chunks
    """
    results = collection.query(
        query_texts=[query],
        n_results=k,
        where={"report_id": report_id}
    )

    return results.get("documents", [[]])[0]
