from langchain_ollama import ChatOllama
from utils.logger import logger
import json

llm = ChatOllama(model="llama3")

def impact_agent(extracted_data: dict) -> dict:
    """
    Impact Agent
    - Analyzes themes & competitors
    """

    logger.info("[Impact] Analysis started")

    prompt = f"""
You are a senior market analyst.

Analyze the following extracted data.
Return STRICT JSON with:
- drivers
- risks
- opportunities
- impacts

DATA:
{json.dumps(extracted_data, indent=2)}

Return ONLY JSON.
"""

    response = llm.invoke(prompt)

    try:
        analysis = json.loads(response.content)
        logger.info("[Impact] LLM analysis completed successfully")
    except Exception:
        logger.error("[Impact] Failed to parse analysis JSON")
        analysis = {
            "drivers": [],
            "risks": [],
            "opportunities": [],
            "impacts": []
        }

    return {
        "topic": extracted_data.get("topic"),
        "analysis": analysis,
        "source_data": extracted_data
    }
