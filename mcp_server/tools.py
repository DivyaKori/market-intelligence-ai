import trafilatura
import requests
import json
from langchain_ollama import ChatOllama
from utils.logger import logger   

llm = ChatOllama(model="llama3")


# -------------------------------------------------
# 1. SEARCH (lightweight – query formulation)
# -------------------------------------------------
def search_web(query: str):
    """
    Returns search intent.
    (Real search engines can be plugged later)
    """
    logger.info(f"[MCP][search_web] Query received: {query}")

    return {
        "query": query,
        "note": "Search layer placeholder – URLs provided by agent or config"
    }


# -------------------------------------------------
# 2. SCRAPE REAL WEB CONTENT
# -------------------------------------------------
def fetch_url(url: str):
    """
    Downloads and extracts clean article text using Trafilatura
    """
    logger.info(f"[MCP][fetch_url] Fetching URL: {url}")

    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise ValueError("Failed to download page")

        text = trafilatura.extract(downloaded)
        if not text:
            raise ValueError("Failed to extract content")

        logger.info(f"[MCP][fetch_url] Successfully scraped: {url}")

        return {
            "url": url,
            "content": text
        }

    except Exception as e:
        logger.error(f"[MCP][fetch_url] Error for {url}: {str(e)}")

        return {
            "url": url,
            "error": str(e),
            "content": ""
        }


# -------------------------------------------------
# 3. CLEAN TEXT
# -------------------------------------------------
def clean_extract(raw_text: str):
    """
    Minimal cleanup – agents + LLM handle intelligence
    """
    logger.info("[MCP][clean_extract] Cleaning raw text")
    return raw_text.strip()


# -------------------------------------------------
# 4. ENTITY EXTRACTION (LLM-DRIVEN)
# -------------------------------------------------
def extract_entities(text: str):
    """
    Uses LLM to extract entities from scraped text
    """
    logger.info("[MCP][extract_entities] Extracting entities via LLM")

    prompt = f"""
Extract key market intelligence entities from the text below.

Return STRICT JSON with:
- competitors
- regulations
- themes
- risks
- opportunities

TEXT:
{text}
"""

    response = llm.invoke(prompt)

    try:
        entities = json.loads(response.content)
        logger.info("[MCP][extract_entities] Entity extraction successful")
        return entities

    except Exception:
        logger.error("[MCP][extract_entities] Failed to parse LLM output")

        return {
            "competitors": [],
            "regulations": [],
            "themes": [],
            "risks": [],
            "opportunities": []
        }


# -------------------------------------------------
# 5. DEDUPLICATION
# -------------------------------------------------
def dedupe_items(items: list):
    logger.info(f"[MCP][dedupe_items] Deduplicating {len(items)} items")
    return list(set(items))


# -------------------------------------------------
# 6. IMPACT SCORING (LLM-DRIVEN, NO STATIC VALUES)
# -------------------------------------------------
def impact_score(item: dict, context: dict):
    """
    LLM decides impact level and score based on REAL context
    """
    logger.info("[MCP][impact_score] Calculating impact score via LLM")

    prompt = f"""
You are a market analyst.

Analyze the following item and context.
Determine:
- impact_level (Low / Medium / High)
- score (0–100)
- why (list of reasons)
- recommended actions

ITEM:
{json.dumps(item, indent=2)}

CONTEXT:
{json.dumps(context, indent=2)}

Return STRICT JSON.
"""

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)
        logger.info("[MCP][impact_score] Impact scoring successful")
        return result

    except Exception:
        logger.error("[MCP][impact_score] Failed to parse impact score")

        return {
            "impact_level": "Unknown",
            "score": None,
            "why": [],
            "actions": []
        }


# -------------------------------------------------
# 7. FINAL REPORT PASS-THROUGH
# -------------------------------------------------
def generate_market_report(data: dict):
    """
    Tools do NOT decide structure.
    Writer agent does.
    """
    logger.info("[MCP][generate_market_report] Passing data to writer agent")
    return data
