from langchain_ollama import ChatOllama
from mcp_server import tools
from utils.logger import logger
import json

llm = ChatOllama(model="llama3")

def collector_agent(topic: str) -> dict:
    """
    Collector Agent
    - Decides relevant URLs
    - Scrapes raw content
    """

    logger.info(f"[Collector] Started for topic: {topic}")

    prompt = f"""
You are a market intelligence collector.

Given the topic: "{topic}"

Return STRICT JSON list of authoritative URLs.
Example:
[
  "https://rbi.org.in",
  "https://www.reuters.com"
]
"""

    response = llm.invoke(prompt)

    try:
        urls = json.loads(response.content)
        if not isinstance(urls, list):
            raise ValueError
    except Exception:
        logger.warning("[Collector] Failed to parse URLs from LLM. Using fallback.")
        urls = [
            "https://www.reuters.com",
            "https://www.mckinsey.com"
        ]

    documents = []

    for url in urls:
        data = tools.fetch_url(url)
        if data.get("content"):
            documents.append({
                "url": url,
                "content": tools.clean_extract(data["content"])
            })

    logger.info(f"[Collector] Documents collected: {len(documents)}")

    return {
        "topic": topic,
        "sources": urls,
        "documents": documents
    }
