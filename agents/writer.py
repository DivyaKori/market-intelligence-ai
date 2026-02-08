from langchain_ollama import ChatOllama
from utils.logger import logger
import json

llm = ChatOllama(model="llama3")

def writer_agent(impact_data: dict) -> dict:
    """
    Writer Agent
    - Converts analysis to final JSON report
    """

    logger.info("[Writer] Report generation started")

    prompt = f"""
You are a principal market intelligence strategist.

Generate FINAL report in STRICT JSON format.

REQUIRED STRUCTURE:
{{
  "summary": string,
  "drivers": list,
  "competitors": list,
  "impact_radar": list,
  "opportunities": list,
  "risks": list,
  "90_day_plan": {{
    "0_30": list,
    "30_60": list,
    "60_90": list
  }},
  "sources": list
}}

INPUT:
{json.dumps(impact_data, indent=2)}

Return ONLY JSON.
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    # 🔧 CRITICAL FIX: force JSON extraction
    start = content.find("{")
    end = content.rfind("}") + 1

    try:
        result = json.loads(content[start:end])
        logger.info("[Writer] Report generated successfully")
        return result
    except Exception:
        logger.error("[Writer] Failed to parse final report JSON")
        return {
            "summary": "Report generation failed",
            "drivers": [],
            "competitors": [],
            "impact_radar": [],
            "opportunities": [],
            "risks": [],
            "90_day_plan": {"0_30": [], "30_60": [], "60_90": []},
            "sources": []
        }
